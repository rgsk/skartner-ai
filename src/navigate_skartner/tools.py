tools = [
    {
        "type": "function",
        "function": {
            "name": "searchWord",
            "description": "Search a word or to get meaning of a word or to run a prompt against a given word",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "the word we want to search",
                    },
                },
                "required": ["word"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "saveWord",
            "description": "Save the word in the dictionary",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "goToManagePrompts",
            "description": "manage prompts or click manage prompts or go to manage prompts page",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "addNewPrompt",
            "description": "start creating a new prompt or add new prompt, if user has specified the prompt then run the type tool next with prompt specified to type the prompt",
           
        }
    },
    {
        "type": "function",
        "function": {
            "name": "editPrompt",
            "description": "start editing a prompt from a list of prompts",
            "parameters": {
                "type": "object",
                "properties": {
                    "promptId": {
                        "type": "string",
                        "description": "the prompt id we want to edit",
                    },
                },
                "required": ["promptId"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "type",
            "description": "type with keyboard",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "string",
                        "description": "what user wanted to type",
                    },
                },
                "required": ["value"],
            },
        }
    },
   {
        "type": "function",
        "function": {
            "name": "saveThePrompt",
            "description": "save the prompt that we have typed",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "the prompt we want to save, must contain word enclosed in curly brackets like {word}, eg 'list meaning of word {word}, 3 example sentences and antonyms and synonyms', you have to ensure that you add placeholder like {word}",
                    },
                },
                "required": ["prompt"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "selectPromptAsDefault",
            "description": "select one of the prompts from a list of prompts as default",
             "parameters": {
                "type": "object",
                "properties": {
                    "promptId": {
                        "type": "string",
                        "description": "the prompt id we want to set as default",
                    },
                },
                "required": ["promptId"],
            },
        }
    }
]