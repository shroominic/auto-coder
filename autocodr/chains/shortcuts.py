import re
from typing import List, Optional, TypeVar, Type
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import SystemMessage
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)

from autocodr.chains.templates import coding_system_prompt, default_system_message


T = TypeVar("T", bound=BaseModel)


async def get_response(
        instruction: HumanMessagePromptTemplate | str,
        system_instruction: SystemMessage | SystemMessagePromptTemplate = default_system_message,
        schema: Type[T] | None = None,
        # context: list[BaseMessage] = [],
        model: str = "gpt-4",
        verbose: bool = False,
        **input_kwargs
    ) -> T | str:
    """
    Get response from chatgpt for provided instructions.
    """
    return await (
        ChatPromptTemplate.from_messages(  # type: ignore
            [
                system_instruction,
            # ] + context + [
                HumanMessagePromptTemplate.from_template(
                    template=instruction
                ) if isinstance(instruction, str) else instruction
            ]
        ) | ChatOpenAI(
            model=model, 
            verbose=verbose, 
            request_timeout=60*5
        ) | (PydanticOutputParser(pydantic_object=schema) if schema else StrOutputParser())
    ).ainvoke(input_kwargs)


class CodeBlocks(BaseModel):
    """ 
    A model for code blocks returned by chatgpt.
    """
    code_blocks: List[str]
    
    def parse(self, parser: Type[T]) -> T:
        """ 
        Parse the code blocks using the provided parser.
        """
        return parser.parse(self.code_blocks[0])
        

def extract_codeblocks(from_response: str) -> list[str]:
    """ Get all codeblocks from the provided response """
    return [
        codeblock.group(2).strip()
        for codeblock in re.finditer(r"```(\w+)(.*?)```", from_response, re.DOTALL)
    ]


async def get_code_response(
        from_instruction: str,
        **kwargs
    ) -> str:
    """
    Get response from chatgpt for provided instructions.
    """
    response = await get_response(
        from_instruction,
        coding_system_prompt,
        **kwargs
    )
    return extract_codeblocks(response)[0]


def extract_files(from_response: str, list_name: str) -> list:
    """ Get a list of files from the provided response """
    codeblock = extract_codeblock(from_response)
    file_list = re.search(rf"{list_name} = \[(.*?)\]", codeblock, re.DOTALL)
    file_paths = file_list and list(map(str, re.findall(r"\'(.*?)\'", file_list.group(1))))
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
        response = await get_response(from_instruction, system_instruction=system_instruction, **kwargs)
        paths = extract_files(response, list_name)
        if validation and not validation(paths):
            raise Exception("Validation of file paths failed")
        return paths
    except Exception as e:
        if retry > 0:
            print("\nError:", e, "\nRetrying...\n")
            return await get_file_paths(
                from_instruction,
                list_name,
                system_instruction, 
                validation,
                retry-1, 
                **kwargs
            )
        else: raise e


def get_multiple_file_paths(
        from_instruction: str, 
        list_names: List[List[str]],
        system_instruction: str = None,
        validations: List[Optional[callable]] = None,
        retry: int = 3,
        **kwargs
    ) -> list:
    """ 
    Get a list of lists of file paths
    """
    try:
        if not validations: validations = [None] * len(list_names)
        if len(list_names) != len(validations):
            raise Exception("list_names and validations must be the same length")
        response = get_code_response(from_instruction, system_instruction=system_instruction, **kwargs)
        paths = [extract_files(response, list_name) for list_name in list_names]
        for validation, path in zip(validations, paths):
            if validation and not validation(path):
                raise Exception("Validation of file paths failed")
        return paths
    except Exception as e:
        if retry > 0:
            print("\nError:", e, "\nRetrying...\n")
            return get_multiple_file_paths(
                from_instruction,
                list_names,
                system_instruction, 
                validations,
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
    
