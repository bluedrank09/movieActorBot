llm_response = "\n\ny "

filter_llm_response = filter(str.isalpha, llm_response)

print(filter_llm_response)

type_flag = "".join(filter_llm_response)
print(type_flag)