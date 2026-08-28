from pydantic import BaseModel, Field


class User(BaseModel):
  name: str = Field(description="The user's full name", examples=['Alice', 'Ali'])

user = User(
  id='1',
  name='Alice',
  age='25'
)

print(user)