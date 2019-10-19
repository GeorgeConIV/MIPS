import java.util.List;

public class ListWrapper
{
    List<String> strings;
    List<Instruction> instructions;

    public ListWrapper(List<String> strings, List<Instruction> instructions)
    {
        this.strings = strings;
        this.instructions = instructions;
    }

    public List<String> getStrings()
    {
        return strings;
    }

    public List<Instruction> getInstructions()
    {
        return instructions;
    }
}
