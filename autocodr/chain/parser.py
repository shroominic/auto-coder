import re, json

from langchain.schema.output_parser import (
    BaseOutputParser, 
    OutputParserException
)

from autocodr.api.utils import raiser


class CodeBlockOutputParser(BaseOutputParser[list[str]]):
    def parse(self, text: str) -> list[str]:
        return codeblocks if (
            codeblocks := [
                codeblock.group(2).strip()
                for codeblock in re.finditer(r"```(\w+)(.*?)```", text, re.DOTALL)
            ]
        ) else raiser(
            OutputParserException("No code blocks found in response")
        )


class FilePathsOutputParser(BaseOutputParser[dict[str, list[str]]]):
    def parse(self, text: str) -> dict[str, list[str]]:
        return (
            json.loads(json_text.group(1)) 
            if (
                json_text := re.search(r"```json(.*?)```", text, re.DOTALL)
            )
            else raiser(
                OutputParserException("No JSON found in response")
            )
        )