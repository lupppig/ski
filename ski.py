import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions import get_file_content, get_files_info, run_python_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        }
    )
)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the content of a file in the specified working directory",
    parameters=types.Schema(
        type= types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to read content from, relative to the working directory"
            )
        }
    )
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to overwrite contents"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write into file"
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to execute functions",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional argument to pass to the Python file"
                ),
                description="Optional list of arguments for the Python file",
            ),
        },
        required=["file_path"]
    )
)




def call_functon(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:    
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
            "get_file_content": get_file_content.get_file_content,
            "write_file": write_file.write_file,
            "run_python_file": run_python_file.run_python_file,
            "get_files_info": get_files_info.get_files_info
        }

    function_name = function_call.name if function_call.name in function_map.keys() else ""
    if not function_name:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )



 

def main():
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str, help="take in user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args =parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    available_function = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
    )


    for _ in range(20):
        response = client.models.generate_content(
                model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_function],
                system_instruction = system_prompt,
                temperature=0,
                )
        )

        if response is None or response.candidates is None:
            print("malformed response")
            break

        for candidate in response.candidates:
            messages.append(types.Content(role="model", parts=candidate.content.parts))
        for part in candidate.content.parts:
            if part.text:
                print(part.text)
        
        if not response.function_calls:
            break

        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_functon(function_call, args.verbose)
            function_responses.extend(function_call_result.parts)

        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
        



    if args.verbose and response is not None:
        print(f"User prompt: {args.verbose}")
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)



if __name__ == "__main__":
    main()
