import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class Main {

    public static void main(String[] args)
    {
        FileManipulator fileMan = new FileManipulator();
        fileMan.initFileScanner("Test.txt");

        AsmScanner scan = new AsmScanner(fileMan.getListOfTokensWhitespaceDelimited());

        List<Instruction> insts = scan.getInstructions();
        List<String> printed = new ArrayList<>();

        int i = 0;
        while(insts.size() > i)
        {
            printed.add(insts.get(i).getBitstream());
            i++;
        }
        fileMan.writeListOfTokens(printed, Optional.empty());

    }
}
