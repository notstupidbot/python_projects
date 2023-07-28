from titlecase import titlecase

def to_camel_case(input_str):
    return titlecase(input_str.replace('_', ' ')).replace(' ', '')

def main(name,fields):
    # main()
    # print("create_model %s" % name)
    fields = fields.split(',')
    buffer="from sqlalchemy import Column, Integer, String, create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nBase = declarative_base()\n"

    class_name=to_camel_case(name)
    buffer += f"\nclass {class_name}(Base):\n" 
    buffer += f"\t__tablename__ = '{name}'\n\n"
    buffer_repr=""
    buffer += f"\tid=Column(Integer,primary_key=True)\n"

    for field in fields:
        buffer += f"\t{field}=Column(String)\n"
        prop = '{self.'+field+'}'
        buffer_repr += f"{field}={prop},"

    
    buffer += f"\n\tdef __repr__(self):\n"
    buffer += f"\t\treturn f\"<{class_name}({buffer_repr})>\""

    # buffer += '}'
    print(buffer)