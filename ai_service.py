async def generate_character_profile(
    name: str,
    age: int,
    role: str | None,
    description: str | None,
) -> str:

    return f"""
# {name}

## Biography
{name} is a character in Oshi no Ko.
Age: {age}.
Role: {role or "Unknown"}.

## Personality
Personality information has not been generated yet.

## Abilities and Skills
No verified information available.

## Relationships
Relationship information has not been generated yet.

## Interesting Facts
No additional facts available.

## Character Analysis
{name}'s character analysis will be added later.
"""