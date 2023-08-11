from typing import TypeVar
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser, BaseOutputParser, OutputParserException
from langchain.schema import SystemMessage, BaseMessage
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

from autocodr.chain.templates import coding_system_prompt, default_system
from autocodr.chain.parser import CodeBlockOutputParser, FilePathsOutputParser
from autocodr.utils import raiser


T = TypeVar("T")

def _default_parser():
    return StrOutputParser()


async def get_response(
        instruction: HumanMessagePromptTemplate | str,
        system: SystemMessage | SystemMessagePromptTemplate = default_system,
        parser: BaseOutputParser[T] = _default_parser(),
        context: list[BaseMessage] = [],
        model: str = "gpt-4",
        verbose: bool = False,
        retry: int = 3,
        /,
        **input_kwargs
    ) -> T:
    """
    Get response from chatgpt for provided instructions.
    """
    try: 
        return await (
            ChatPromptTemplate.from_messages(
                [
                    system,
                ] + context + [
                    HumanMessagePromptTemplate.from_template(
                        template=instruction
                    ) if isinstance(instruction, str) else instruction
                ]
            ) | ChatOpenAI(
                model=model,
                verbose=verbose, 
                request_timeout=60*5
            ) | parser
        ).ainvoke(input_kwargs)
    
    except OutputParserException as e: 
        return await get_response(
            instruction,
            system=system,
            parser=parser,
            context=context,
            model=model,
            verbose=verbose,
            retry=retry-1,
            **input_kwargs
        ) if retry > 0 else raiser(e)


async def get_code_response(
        from_instruction: HumanMessagePromptTemplate | str,
        with_context: BaseMessage | None = None,
        /,
        **kwargs
    ) -> str:
    return (
        await get_response(
            from_instruction,
            coding_system_prompt,
            parser=CodeBlockOutputParser(),
            context=[with_context] if with_context else [],
            **kwargs
        )
    )[0]


async def get_file_paths(
        from_instruction: HumanMessagePromptTemplate | str,
        list_name: str,
        system_instruction=coding_system_prompt,
        **kwargs
    ) -> list[str]:
    """ 
    Get a list of file paths from the provided instruction 
    """
    return (
        await get_response(
            from_instruction, 
            system_instruction=system_instruction,
            parser=FilePathsOutputParser(),
            **kwargs
        )
    )[list_name]


async def get_multiple_file_paths(
        from_instruction: HumanMessagePromptTemplate | str,
        system_instruction=coding_system_prompt,
        **kwargs
    ) -> dict[str, list[str]]:
    """ 
    Get a list of file paths from the provided instruction 
    """
    return await get_response(
        from_instruction, 
        system_instruction=system_instruction,
        parser=FilePathsOutputParser(),
        **kwargs
    )


async def gpt_format(file):
    cleanup_prompt = (
        "Rewrite the following file to match proper formatting.\n"
        "Do not change the code or contents, only the appearance.\n"
        "If the file is already properly formatted, return the same file.\n"
        "Reply with a codeblock containing the formatted file.\n\n"
        "```\n{file}\n```"
    )

    return await get_code_response(cleanup_prompt, file=file)


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    
    print(asyncio.run(get_code_response(
        "Write a function that computes pi without using any module."
    )))
