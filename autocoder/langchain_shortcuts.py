import re
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


async def get_response(
        from_instruction: str, 
        system_instruction: str = None,
        validation=None,
        model="gpt-4", 
        verbose=False, 
        retry=0,
        **kwargs
    ) -> str:
    """
    Get response from chatgpt for provided instructions.
    """
    try:
        chatgpt = ChatOpenAI(model=model, verbose=verbose, request_timeout=60*5, **kwargs)
        system = SystemMessagePromptTemplate.from_template(
            template=system_instruction or
            "Follow the instructions provided by the user. "
            "Answer precise, efficient and accurate."
        )
        user = HumanMessagePromptTemplate.from_template(template=from_instruction)
        prompt = ChatPromptTemplate.from_messages([system, user])
        chain = LLMChain(llm=chatgpt, prompt=prompt, verbose=verbose)
        output = await chain.arun(kwargs)
        if validation and not validation(output): 
            raise Exception("Validation failed")
        return output
    except Exception as e:
        if retry > 0:
            print("\nError:", e, "\nRetrying...\n")
            return await get_response(prompt, model, verbose, retry-1, **kwargs)
        else: raise e


def extract_codeblock(from_response: str) -> str:
    """ Get a codeblock from the provided response """
    codeblock = re.search(r"```(\w+)(.*?)```", from_response, re.DOTALL)
    # TODO: multiple codeblocks could be returned
    if codeblock: return codeblock.group(2).strip()
    else: raise Exception("No codeblock found")


async def get_code_response(
        from_instruction: str, 
        system_instruction: str = None,
        validation=None,
        retry=1,
        **kwargs
    ) -> str:
    """
    Get response from chatgpt for provided instructions.
    """
    try: 
        response = await get_response(
            from_instruction, 
            system_instruction, 
            validation, 
            retry, 
            **kwargs
        )
        return extract_codeblock(response)
    except Exception as e:
        if retry > 0:
            print("\nError:", e, "\nRetrying...\n")
            return await get_code_response(
                from_instruction, 
                system_instruction, 
                validation, 
                retry-1, 
                **kwargs
            )
        else: raise e


def extract_files(from_response: str, list_name: str) -> list:
    """ Get a list of files from the provided response """
    codeblock = extract_codeblock(from_response)
    file_list = re.search(rf"{list_name} = \[(.*?)\]", codeblock, re.DOTALL)
    file_paths = file_list and re.findall(r"\'(.*?)\'", file_list.group(1))
    return file_paths


async def get_file_paths(
        from_instruction: str, 
        list_name: str,
        system_instruction: str = None,
        validation=None,
        retry=3,
        **kwargs
    ) -> list:
    """ 
    Get a list of file paths from the provided instruction 
    """
    try:
        response = await get_response(from_instruction, **kwargs)
        paths = extract_files(response, list_name)
        if validation and not validation(paths):
            raise Exception("Validation of file paths failed")
        return paths
    except Exception as e:
        if retry > 0:
            print("\nError:", e, "\nRetrying...\n")
            return await get_file_paths(
                from_instruction, 
                system_instruction, 
                retry-1, 
                **kwargs
            )
        else: raise e
    

async def gpt_format(file):
    """ format file using chatgpt to get a clean result """
    cleanup_prompt = """
    Rewrite the following file to match proper formatting.
    Do not change the code or contents, only the appearance.
    If the file is already properly formatted, return the same file.
    Reply with a codeblock containing the formatted file.
    
    ```
    {file}
    ```
    """
    return await get_code_response(cleanup_prompt, file=file)


# testing
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    
    example_prompt = "Write a function that computes pi without using any module."
    output = asyncio.run(get_code_response(example_prompt))
    print(output)
    
