"""jsonschema for functions"""

_SCHEMAS = {
    "answer_collector": {
        "report_bool": {
            "description": "Report answer in bool " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "bool " "format.",
                    "type": "boolean",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_dict": {
            "description": "Report answer in dict " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "dict " "format.",
                    "type": ["object"],
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_float": {
            "description": "Report answer in " "string format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "float " "format.",
                    "type": "number",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_int": {
            "description": "Report answer in " "integer format",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "integer " "format.",
                    "type": "integer",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_json": {
            "description": "Report answer in json " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "json " "format.",
                    "type": "string",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_list": {
            "description": "Report answer in list " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "list " "format.",
                    "type": "string",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_set": {
            "description": "Report answer in set " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "set " "format.",
                    "type": "array",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_text": {
            "description": "Report answer in " "string format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "string " "format.",
                    "type": "string",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_toml": {
            "description": "Report answer in toml " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "toml " "format.",
                    "type": "string",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_tuple": {
            "description": "Report answer in " "tuple format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "tuple " "format.",
                    "type": "array",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
        "report_xml": {
            "description": "Report answer in xml " "format.",
            "properties": {
                "answer": {
                    "description": "The " "answer " "to " "be " "reported " "in " "xml " "format.",
                    "type": "string",
                },
                "comment": {
                    "default": "",
                    "description": "Any " "comments, " "supplemental " "info " "about " "the " "answer.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["answer"],
            "type": "object",
        },
    },
    "cat": {
        "cat": {
            "description": "Mimics the basic functionalities of the " "'cat' command in Unix.",
            "properties": {
                "file_paths": {"description": "A list of " "file paths " "to " "concatenate.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside the "
                    "JSON.",
                    "type": "string",
                },
                "number_lines": {
                    "default": True,
                    "description": "If True, " "number " "all " "output " "lines.",
                    "type": "boolean",
                },
                "squeeze_blank": {
                    "default": False,
                    "description": "If " "True, " "consecutive " "blank " "lines " "are " "squeezed " "to one.",
                    "type": "boolean",
                },
            },
            "required": ["file_paths"],
            "type": "object",
        },
        "cat_markdown": {
            "description": "Concatenates the content of given " "file paths and formats them as " "markdown.",
            "properties": {
                "file_paths": {"description": "List " "of " "file " "paths " "to " "concatenate.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "number_lines": {
                    "default": True,
                    "description": "If " "True, " "number " "all " "output " "lines.",
                    "type": "boolean",
                },
                "squeeze_blank": {
                    "default": False,
                    "description": "If " "True, " "consecutive " "blank " "lines " "are " "squeezed " "to " "one.",
                    "type": "boolean",
                },
            },
            "required": ["file_paths"],
            "type": "object",
        },
    },
    "cut": {
        "cut_characters": {
            "description": "Reads a file and extracts " "characters based on specified " "ranges.",
            "properties": {
                "character_ranges": {
                    "description": "A " "string " "representing " "character " "ranges, " "e.g., " '"1-5,10".',
                    "type": "string",
                },
                "file_path": {"description": "The " "name " "of " "the " "file " "to " "process.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path", "character_ranges"],
            "type": "object",
        },
        "cut_fields": {
            "description": "Reads a file and extracts fields "
            "based on specified ranges using the "
            "given delimiter.",
            "properties": {
                "delimiter": {
                    "default": ",",
                    "description": "A " "single " "character " "used " "as " "the " "field " "delimiter.",
                    "type": "string",
                },
                "field_ranges": {
                    "description": "A " "string " "representing " "field " "ranges, " "e.g., " '"1-3,5".',
                    "type": "string",
                },
                "filename": {"description": "The " "name " "of " "the " "file " "to " "process.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["filename", "field_ranges"],
            "type": "object",
        },
        "cut_fields_by_name": {
            "description": "Reads a file and extracts "
            "fields based on specified "
            "field names using the given "
            "delimiter.",
            "properties": {
                "delimiter": {
                    "default": ",",
                    "description": "A " "single " "character " "used " "as " "the " "field " "delimiter.",
                    "type": "string",
                },
                "field_names": {"description": "A " "list " "of " "field " "names " "to " "extract.", "type": "string"},
                "filename": {"description": "The " "name " "of " "the " "file " "to " "process.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["filename", "field_names"],
            "type": "object",
        },
    },
    "ed": {
        "ed": {
            "description": "A python version of ed.",
            "properties": {
                "file_name": {"description": "Script " "creates or " "edits this " "file.", "type": "string"},
                "mime_type": {
                    "description": "Return value "
                    "as text/csv, "
                    "text/markdown, "
                    "or text/yaml "
                    "inside the "
                    "JSON.",
                    "type": "string",
                },
                "script": {"description": "Ed commands to " "run.", "type": "string"},
            },
            "required": ["script", "file_name"],
            "type": "object",
        }
    },
    "edlin": {
        "edlin": {
            "description": "An improved version of the edlin.",
            "properties": {
                "file_name": {"description": "Script " "creates " "or " "edits " "this " "file.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "script": {"description": "Edlin " "commands " "to run.", "type": "string"},
            },
            "required": ["script", "file_name"],
            "type": "object",
        }
    },
    "find": {
        "find_files": {
            "description": "Recursively search for files or "
            "directories matching given "
            "criteria in a directory and its "
            "subdirectories.",
            "properties": {
                "file_type": {
                    "description": "The " "type " "to " "filter " "('file' " "or " "'directory').",
                    "type": ["string", "null"],
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "name": {
                    "description": "The " "exact " "name to " "match " "filenames " "against.",
                    "type": ["string", "null"],
                },
                "regex": {
                    "description": "The " "regex " "pattern " "to " "match " "filenames " "against.",
                    "type": ["string", "null"],
                },
                "size": {
                    "description": "The size "
                    "to "
                    "filter "
                    "files "
                    "by, "
                    "e.g., "
                    "'+100' "
                    "for "
                    "files "
                    "larger "
                    "than 100 "
                    "bytes.",
                    "type": ["string", "null"],
                },
            },
            "required": ["name", "regex", "file_type", "size"],
            "type": "object",
        },
        "find_files_markdown": {
            "description": "Recursively search for "
            "files or directories "
            "matching given criteria "
            "in a directory and its "
            "subdirectories.",
            "properties": {
                "file_type": {
                    "description": "The " "type " "to " "filter " "('file' " "or " "'directory').",
                    "type": ["string", "null"],
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "name": {
                    "description": "The " "exact " "name " "to " "match " "filenames " "against.",
                    "type": ["string", "null"],
                },
                "regex": {
                    "description": "The " "regex " "pattern " "to " "match " "filenames " "against.",
                    "type": ["string", "null"],
                },
                "size": {
                    "description": "The "
                    "size "
                    "to "
                    "filter "
                    "files "
                    "by, "
                    "e.g., "
                    "'+100' "
                    "for "
                    "files "
                    "larger "
                    "than "
                    "100 "
                    "bytes.",
                    "type": ["string", "null"],
                },
            },
            "required": ["name", "regex", "file_type", "size"],
            "type": "object",
        },
    },
    "git": {
        "get_current_branch": {
            "description": "Retrieves the current " "branch name of the " "repository.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        },
        "get_recent_commits": {
            "description": "Retrieves the most recent " "commit hashes from the " "current branch.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "n": {
                    "default": 10,
                    "description": "The "
                    "number "
                    "of "
                    "recent "
                    "commits "
                    "to "
                    "retrieve. "
                    "Defaults "
                    "to "
                    "10.",
                    "type": "integer",
                },
                "short_hash": {
                    "default": False,
                    "description": "If "
                    "True, "
                    "return "
                    "short "
                    "hashes; "
                    "otherwise, "
                    "return "
                    "full "
                    "hashes. "
                    "Defaults "
                    "to "
                    "False.",
                    "type": "boolean",
                },
            },
            "required": [],
            "type": "object",
        },
        "git_diff": {
            "description": "Returns the differences in the " "working directory.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        },
        "git_diff_commit": {
            "description": "Shows changes between two " "commits.",
            "properties": {
                "commit1": {"description": "First " "commit", "type": "string"},
                "commit2": {"description": "Second " "commit", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["commit1", "commit2"],
            "type": "object",
        },
        "git_log_file": {
            "description": "Returns the commit history for a " "specific file.",
            "properties": {
                "filename": {"description": "The " "path " "to " "the " "file.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["filename"],
            "type": "object",
        },
        "git_log_search": {
            "description": "Returns the commit history that " "matches the search string.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "search_string": {"description": "The " "search " "string.", "type": "string"},
            },
            "required": ["search_string"],
            "type": "object",
        },
        "git_show": {
            "description": "Shows various types of objects " "(commits, tags, etc.).",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        },
        "git_status": {
            "description": "Returns the status of the " "repository.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        },
        "is_ignored_by_gitignore": {
            "description": "Check if a file is " "ignored by .gitignore.",
            "properties": {
                "file_path": {"description": "The " "path " "of " "the " "file " "to " "check.", "type": "string"},
                "gitignore_path": {
                    "default": ".gitignore",
                    "description": "The "
                    "path "
                    "to "
                    "the "
                    ".gitignore "
                    "file. "
                    "Defaults "
                    "to "
                    "'.gitignore' "
                    "in "
                    "the "
                    "current "
                    "directory.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path"],
            "type": "object",
        },
    },
    "grep": {
        "grep": {
            "description": "Search for lines matching a regular " "expression in files specified by a glob " "pattern.",
            "properties": {
                "glob_pattern": {
                    "description": "A glob " "pattern " "string " "to " "specify " "files.",
                    "type": "string",
                },
                "maximum_matches_per_file": {
                    "default": -1,
                    "description": "Maximum " "number " "of " "matches " "to " "return " "for " "one " "file.",
                    "type": "integer",
                },
                "maximum_matches_total": {
                    "default": -1,
                    "description": "Maximum " "number " "of " "matches " "to " "return " "total.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the JSON.",
                    "type": "string",
                },
                "regex": {"description": "A regular " "expression " "string to " "search for.", "type": "string"},
                "skip_first_matches": {
                    "default": -1,
                    "description": "Number " "of " "initial " "matches " "to " "skip.",
                    "type": "integer",
                },
            },
            "required": ["regex", "glob_pattern"],
            "type": "object",
        },
        "grep_markdown": {
            "description": "Search for lines matching a "
            "regular expression in files and "
            "returns markdown formatted "
            "results.",
            "properties": {
                "glob_pattern": {
                    "description": "A " "glob " "pattern " "string " "to " "specify " "files.",
                    "type": "string",
                },
                "maximum_matches": {
                    "default": -1,
                    "description": "Maximum " "number " "of " "matches " "to " "return.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "regex": {
                    "description": "A " "regular " "expression " "string " "to " "search " "for.",
                    "type": "string",
                },
                "skip_first_matches": {
                    "default": -1,
                    "description": "Number " "of " "initial " "matches " "to " "skip.",
                    "type": "integer",
                },
            },
            "required": ["regex", "glob_pattern"],
            "type": "object",
        },
    },
    "headtail": {
        "head": {
            "description": "Return the first 'lines' or " "'byte_count' from a file.",
            "properties": {
                "byte_count": {
                    "description": "Number " "of " "bytes " "to " "return. " "If " "specified, " "overrides " "lines.",
                    "type": ["integer", "null"],
                },
                "file_path": {"description": "Path " "to " "the " "file.", "type": "string"},
                "lines": {
                    "default": 10,
                    "description": "Number of "
                    "lines to "
                    "return. "
                    "Ignored "
                    "if "
                    "byte_count "
                    "is "
                    "specified. "
                    "Defaults "
                    "to 10.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path", "byte_count"],
            "type": "object",
        },
        "head_markdown": {
            "description": "Return the first 'lines' " "lines of a file formatted " "as markdown.",
            "properties": {
                "file_path": {"description": "Path " "to " "the " "file.", "type": "string"},
                "lines": {
                    "default": 10,
                    "description": "Number " "of " "lines " "to " "return. " "Defaults " "to " "10.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path"],
            "type": "object",
        },
        "head_tail": {
            "description": "Read lines or bytes from the " "start ('head') or end ('tail') " "of a file.",
            "properties": {
                "byte_count": {
                    "description": "Number " "of " "bytes " "to " "read. " "If " "specified, " "overrides " "lines.",
                    "type": ["integer", "null"],
                },
                "file_path": {"description": "Path " "to " "the " "file.", "type": "string"},
                "lines": {
                    "default": 10,
                    "description": "Number "
                    "of "
                    "lines "
                    "to "
                    "read. "
                    "Ignored "
                    "if "
                    "byte_count "
                    "is "
                    "specified. "
                    "Defaults "
                    "to "
                    "10.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "mode": {
                    "default": "head",
                    "description": "Operation "
                    "mode, "
                    "either "
                    "'head' "
                    "or "
                    "'tail'. "
                    "Defaults "
                    "to "
                    "'head'.",
                    "type": "string",
                },
            },
            "required": ["file_path", "byte_count"],
            "type": "object",
        },
        "tail": {
            "description": "Return the last 'lines' or 'bytes' " "from a file.",
            "properties": {
                "byte_count": {
                    "description": "Number " "of " "bytes " "to " "return. " "If " "specified, " "overrides " "lines.",
                    "type": ["integer", "null"],
                },
                "file_path": {"description": "Path " "to " "the " "file.", "type": "string"},
                "lines": {
                    "default": 10,
                    "description": "Number of "
                    "lines to "
                    "return. "
                    "Ignored "
                    "if "
                    "byte_count "
                    "is "
                    "specified. "
                    "Defaults "
                    "to 10.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path", "byte_count"],
            "type": "object",
        },
        "tail_markdown": {
            "description": "Return the last 'lines' " "lines of a file formatted " "as markdown.",
            "properties": {
                "file_path": {"description": "Path " "to " "the " "file.", "type": "string"},
                "lines": {
                    "default": 10,
                    "description": "Number " "of " "lines " "to " "return. " "Defaults " "to " "10.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path"],
            "type": "object",
        },
    },
    "insert": {
        "insert_text_after_context": {
            "description": "Inserts a given " "text immediately " "after a specified " "context in a " "file.",
            "properties": {
                "context": {
                    "description": "The "
                    "context "
                    "string "
                    "to "
                    "search "
                    "for "
                    "in "
                    "the "
                    "file. "
                    "The "
                    "text "
                    "is\n"
                    "inserted "
                    "after "
                    "the "
                    "line "
                    "containing "
                    "this "
                    "context.",
                    "type": "string",
                },
                "file_path": {
                    "description": "The "
                    "path "
                    "of "
                    "the "
                    "file "
                    "in "
                    "which "
                    "the "
                    "text "
                    "is "
                    "to "
                    "be "
                    "inserted.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "text_to_insert": {
                    "description": "The " "text " "to " "insert " "into " "the " "file.",
                    "type": "string",
                },
            },
            "required": ["file_path", "context", "text_to_insert"],
            "type": "object",
        },
        "insert_text_after_multiline_context": {
            "description": "Inserts "
            "text "
            "immediately "
            "after a "
            "specified "
            "multiline "
            "context "
            "in a "
            "file.",
            "properties": {
                "context_lines": {
                    "description": "A "
                    "list "
                    "of "
                    "strings "
                    "representing "
                    "the "
                    "multiline\n"
                    "context "
                    "to "
                    "search "
                    "for "
                    "in "
                    "the "
                    "file.",
                    "type": "string",
                },
                "file_path": {
                    "description": "The "
                    "path "
                    "of "
                    "the "
                    "file "
                    "in "
                    "which "
                    "the "
                    "text "
                    "is "
                    "to "
                    "be "
                    "inserted.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "text_to_insert": {
                    "description": "The " "text " "to " "insert " "into " "the " "file " "after " "the " "context.",
                    "type": "string",
                },
            },
            "required": ["file_path", "context_lines", "text_to_insert"],
            "type": "object",
        },
        "insert_text_at_start_or_end": {
            "description": "Inserts text at " "the start or " "end of a file.",
            "properties": {
                "file_path": {
                    "description": "The "
                    "path "
                    "of "
                    "the "
                    "file "
                    "in "
                    "which "
                    "the "
                    "text "
                    "is "
                    "to "
                    "be "
                    "inserted.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "position": {
                    "default": "end",
                    "description": "The "
                    "position "
                    "where "
                    "the "
                    "text "
                    "should "
                    "be "
                    "inserted.\n"
                    "Should "
                    "be "
                    "either "
                    "'start' "
                    "or "
                    "'end'. "
                    "Defaults "
                    "to "
                    "'end'.",
                    "type": "string",
                },
                "text_to_insert": {
                    "description": "The " "text " "to " "insert " "into " "the " "file.",
                    "type": "string",
                },
            },
            "required": ["file_path", "text_to_insert"],
            "type": "object",
        },
    },
    "ls": {
        "ls": {
            "description": "List directory contents, with options to " "include all files and detailed view.",
            "properties": {
                "all_files": {
                    "default": False,
                    "description": "If True, " "include " "hidden files. " "Defaults to " "False.",
                    "type": "boolean",
                },
                "long": {
                    "default": False,
                    "description": "If True, include "
                    "details like "
                    "permissions, "
                    "owner, size, and "
                    "modification date. "
                    "Defaults to False.",
                    "type": "boolean",
                },
                "mime_type": {
                    "description": "Return value "
                    "as text/csv, "
                    "text/markdown, "
                    "or text/yaml "
                    "inside the "
                    "JSON.",
                    "type": "string",
                },
                "path": {
                    "description": "The directory path " "to list. Defaults " "to the current " "directory '.'.",
                    "type": ["string", "null"],
                },
            },
            "required": ["path"],
            "type": "object",
        },
        "ls_markdown": {
            "description": "List directory contents, with " "options to include all files and " "detailed view.",
            "properties": {
                "all_files": {
                    "default": False,
                    "description": "If " "True, " "include " "hidden " "files. " "Defaults " "to " "False.",
                    "type": "boolean",
                },
                "long": {
                    "default": False,
                    "description": "If True, "
                    "include "
                    "details "
                    "like "
                    "permissions, "
                    "owner, "
                    "size, and "
                    "modification "
                    "date. "
                    "Defaults "
                    "to False.",
                    "type": "boolean",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "path": {
                    "default": ".",
                    "description": "The "
                    "directory "
                    "path to "
                    "list. "
                    "Defaults "
                    "to the "
                    "current "
                    "directory "
                    "'.'.",
                    "type": ["string", "null"],
                },
            },
            "required": [],
            "type": "object",
        },
    },
    "patch": {
        "apply_git_patch": {
            "description": "Apply a git patch to the " "files in the root folder.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "patch_content": {"description": "The " "content " "of " "the " "git " "patch.", "type": "string"},
            },
            "required": ["patch_content"],
            "type": "object",
        }
    },
    "pycat": {
        "format_code_as_markdown": {
            "description": "Combine all Python " "files in a directory " "into a single " "Markdown file.",
            "properties": {
                "base_path": {
                    "description": "The " "base " "path " "of " "the " "directory " "to " "start " "traversing.",
                    "type": "string",
                },
                "header": {
                    "description": "A "
                    "header "
                    "string "
                    "to "
                    "be "
                    "included "
                    "at "
                    "the "
                    "beginning "
                    "of "
                    "the "
                    "Markdown "
                    "file.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "no_comments": {
                    "default": False,
                    "description": "Whether "
                    "to "
                    "exclude "
                    "comments "
                    "from "
                    "the "
                    "output. "
                    "Defaults "
                    "to "
                    "False.",
                    "type": "boolean",
                },
                "no_docs": {
                    "default": False,
                    "description": "Whether "
                    "to "
                    "exclude "
                    "docstrings "
                    "from "
                    "the "
                    "output. "
                    "Defaults "
                    "to "
                    "False.",
                    "type": "boolean",
                },
            },
            "required": ["base_path", "header"],
            "type": "object",
        }
    },
    "pytest": {
        "pytest": {
            "description": "Runs pytest on tests in tests " "folder..",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        }
    },
    "replace": {
        "replace_all": {
            "description": "Replaces all occurrences of a " "specified text with new text " "in a file.",
            "properties": {
                "file_path": {"description": "The " "path " "to " "the " "file.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "new_text": {
                    "description": "The " "new " "text " "to " "replace " "the " "old " "text.",
                    "type": "string",
                },
                "old_text": {"description": "The " "text " "to " "be " "replaced.", "type": "string"},
            },
            "required": ["file_path", "old_text", "new_text"],
            "type": "object",
        },
        "replace_line_by_line": {
            "description": "Replaces occurrences "
            "of a specified text "
            "with new text in a "
            "range of lines in a "
            "file.",
            "properties": {
                "file_path": {"description": "The " "path " "to " "the " "file.", "type": "string"},
                "line_end": {
                    "default": -1,
                    "description": "The "
                    "ending "
                    "line "
                    "number "
                    "(0-indexed) "
                    "for "
                    "the "
                    "replacement.\n"
                    "If "
                    "-1, "
                    "it "
                    "goes "
                    "to "
                    "the "
                    "end "
                    "of "
                    "the "
                    "file. "
                    "Defaults "
                    "to "
                    "-1.",
                    "type": "integer",
                },
                "line_start": {
                    "default": 0,
                    "description": "The "
                    "starting "
                    "line "
                    "number "
                    "(0-indexed) "
                    "for "
                    "the "
                    "replacement.\n"
                    "Defaults "
                    "to "
                    "0.",
                    "type": "integer",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "new_text": {
                    "description": "The " "new " "text " "to " "replace " "the " "old " "text.",
                    "type": "string",
                },
                "old_text": {"description": "The " "text " "to " "be " "replaced.", "type": "string"},
            },
            "required": ["file_path", "old_text", "new_text"],
            "type": "object",
        },
        "replace_with_regex": {
            "description": "Replaces text in a file " "based on a regular " "expression match.",
            "properties": {
                "file_path": {"description": "The " "path " "to " "the " "file.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "regex_match_expression": {
                    "description": "The " "regular " "expression " "pattern " "to " "match.",
                    "type": "string",
                },
                "replacement": {
                    "description": "The " "text " "to " "replace " "the " "matched " "pattern.",
                    "type": "string",
                },
            },
            "required": ["file_path", "regex_match_expression", "replacement"],
            "type": "object",
        },
        "save_if_changed": {
            "description": "Saves the modified text to " "the file if changes have " "been made.",
            "properties": {
                "file_path": {"description": "The " "path " "to " "the " "file.", "type": "string"},
                "final": {"description": "The " "modified " "text.", "type": "string"},
                "input_text": {"description": "The " "original " "text.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path", "final", "input_text"],
            "type": "object",
        },
    },
    "rewrite": {
        "revert_to_latest_backup": {
            "description": "Revert the file to " "the most recent " "backup.",
            "properties": {
                "file_name": {"description": "The " "name " "of " "the " "file " "to " "revert.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_name"],
            "type": "object",
        },
        "rewrite_file": {
            "description": "Backup and rewrite an " "existing file at file_path " "within the root_folder.",
            "properties": {
                "file_path": {
                    "description": "The " "relative " "path " "to " "the " "file " "to " "be " "rewritten.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "text": {
                    "description": "The " "new " "content " "to " "write " "into " "the " "file.",
                    "type": "string",
                },
            },
            "required": ["file_path", "text"],
            "type": "object",
        },
        "write_new_file": {
            "description": "Write a new file at " "file_path within the " "root_folder.",
            "properties": {
                "file_path": {
                    "description": "The " "relative " "path " "to " "the " "file " "to " "be " "written.",
                    "type": "string",
                },
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "text": {"description": "The " "content " "to " "write " "into " "the " "file.", "type": "string"},
            },
            "required": ["file_path", "text"],
            "type": "object",
        },
    },
    "sed": {
        "sed": {
            "description": "Transform the contents of a file located "
            "at file_path as per the provided sed-like "
            "commands.",
            "properties": {
                "commands": {
                    "description": "A list of " "sed-like " "commands for " "text " "transformation.",
                    "type": "string",
                },
                "file_path": {"description": "The path of " "the file to " "be " "transformed.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside the "
                    "JSON.",
                    "type": "string",
                },
            },
            "required": ["file_path", "commands"],
            "type": "object",
        }
    },
    "todo": {
        "add_todo": {
            "description": "Adds a new task to the task manager.",
            "properties": {
                "assignee": {
                    "description": "The " "name " "of the " "assignee. " "Defaults " "to " "None.",
                    "type": ["string", "null"],
                },
                "category": {
                    "description": "The " "category " "of the " "task " "(e.g., " "'bug', " "'feature').",
                    "type": "string",
                },
                "description": {"description": "A " "description " "of " "the " "task.", "type": "string"},
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "source_code_ref": {
                    "description": "Reference " "to " "the " "source " "code " "related " "to " "the " "task.",
                    "type": "string",
                },
                "title": {"description": "The title " "of the " "task.", "type": "string"},
            },
            "required": ["title", "description", "category", "source_code_ref", "assignee"],
            "type": "object",
        },
        "query_todos_by_assignee": {
            "description": "Queries tasks "
            "assigned to a "
            "specific assignee. "
            "Currently, the "
            "assignee is "
            "hard-coded as "
            "'Developer'.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                }
            },
            "required": [],
            "type": "object",
        },
        "query_todos_by_regex": {
            "description": "Queries tasks by a " "keyword in their title, " "using a regular " "expression pattern.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "regex_pattern": {
                    "default": "[\\s\\S]+",
                    "description": "The "
                    "regular "
                    "expression "
                    "pattern "
                    "to "
                    "match "
                    "in "
                    "task "
                    "titles.\n"
                    "Defaults "
                    "to "
                    '"[\\s\\S]+", '
                    "which "
                    "matches "
                    "any "
                    "title.",
                    "type": "string",
                },
            },
            "required": [],
            "type": "object",
        },
        "remove_todo": {
            "description": "Marks a task as finished based on " "its title.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "title": {
                    "description": "The " "title " "of the " "task " "to be " "marked " "as " "finished.",
                    "type": "string",
                },
            },
            "required": ["title"],
            "type": "object",
        },
    },
    "token_counter": {
        "count_tokens": {
            "description": "Count the number of " "tokens in a string.",
            "properties": {
                "mime_type": {
                    "description": "Return "
                    "value "
                    "as "
                    "text/csv, "
                    "text/markdown, "
                    "or "
                    "text/yaml "
                    "inside "
                    "the "
                    "JSON.",
                    "type": "string",
                },
                "text": {"description": "The " "text " "to " "count " "the " "tokens " "in.", "type": "string"},
            },
            "required": ["text"],
            "type": "object",
        }
    },
}
