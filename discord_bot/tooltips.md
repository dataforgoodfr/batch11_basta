# How to do a command with multiple parameters

```python
class test_command_flags(commands.FlagConverter):
    sentence: typing.Optional[str] = commands.flag(
        description="Insert here the bot response."
    )

# Reply to the user sending the command the parameter of the command
@commands.hybrid_command(
    name="testopt", description="Test command with an optional argument"
)
async def testOpt(ctx, *, flags: test_command_flags):
    if flags.sentence:
        await ctx.reply(flags.sentence)
```