import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;

public class AsmScanner
{
    List<String> instructions;
    Integer currentListLoc = 0;
    Integer currentLineLoc = 0;
    Integer prevPosition[] = {0, 0};
    Character charBuff = ' ';
    Instruction thing;
    HashMap<String, Integer> label_map = new HashMap<>();
    Integer pc = 0;

    public AsmScanner(List<String> instructions)
    {
        this.instructions = instructions;
    }


    public Character getChar()
    {
        prevPosition[0] = currentListLoc;
        prevPosition[1] = currentLineLoc;
        if(instructions.get(currentListLoc).length() == currentLineLoc && ((instructions.size() - 1) == currentListLoc))
        {
            return '\0';
        }
        if(instructions.get(currentListLoc).length() == currentLineLoc)
        {
            currentListLoc++;
            currentLineLoc = 0;
            return '\n';
        }

        Character c = instructions.get(currentListLoc).charAt(currentLineLoc);
        currentLineLoc++;

        return c;
    }

    public Instruction getLabel()
    {

    }


    public Instruction getInstruction()
    {
        String inst = "";
        String cond = "";
        charBuff = getChar();
        Instruction in = new Instruction(instructions.get(currentLineLoc));
        while(Character.isWhitespace(charBuff) && (charBuff != '\0'))
        {
            if(charBuff == '\n')
            {
                break;
            }
            charBuff = getChar();
        }

        if(Character.isLetter(charBuff))
        {
            do{
                inst += charBuff;
                charBuff = getChar();
            }while(Character.isLetter(charBuff));

            if(inst.endsWith(":"))
            {
                label_map.put(inst, pc);
                return null;
            }

            if(inst.endsWith("NE"))
            {
                in.setCond("001");
                inst = inst.replaceAll("NE", "");
            }
            else if(inst.endsWith("EQ"))
            {
                in.setCond("010");
                inst = inst.replaceAll("EQ", "");
            }
            else if(inst.endsWith("LT"))
            {
                in.setCond("011");
                inst = inst.replaceAll("LT", "");
            }
            else if(inst.endsWith("GT"))
            {
                in.setCond("100");
                inst = inst.replaceAll("GT", "");
            }
            else if(inst.endsWith("LTE"))
            {
                in.setCond("101");
                inst = inst.replaceAll("LTE", "");
            }
            else if(inst.endsWith("GTE"))
            {
                in.setCond("110");
                inst = inst.replaceAll("GTE", "");
            }
            else if(inst.endsWith("EQZ"))
            {
                in.setCond("111");
                inst = inst.replaceAll("EQZ", "");
            }
            else
            {
                in.setCond("000");
            }

            switch(inst)
            {                
                case "NOP" :
                    in.setOpcode("00000");
                    in.setImm("00000000000");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    return in;
                case "ADD" :
                    in.setOpcode("00001");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "ADDI" :
                    in.setOpcode("00010");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "SUB" :
                    in.setOpcode("00011");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "SUBI" :
                    in.setOpcode("00100");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "MUL" :
                    in.setOpcode("00101");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "MULI" :
                    in.setOpcode("00110");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "DIV" :
                    in.setOpcode("00111");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "DIVI" :
                    in.setOpcode("01000");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "LSL" :
                    in.setOpcode("01001");
                    in.setType("000");
                    in.setInType(Instruction.instType.SHIFT);
                    break;
                case "LSR" :
                    in.setOpcode("01001");
                    in.setType("001");
                    in.setInType(Instruction.instType.SHIFT);
                    break;
                case "ASR" :
                    in.setOpcode("01001");
                    in.setType("010");
                    in.setInType(Instruction.instType.SHIFT);
                    break;
                case "TAR" :
                    in.setOpcode("01010");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "MOV" :
                    in.setOpcode("01011");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "CMP" :
                    in.setOpcode("01100");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "AND" :
                    in.setOpcode("01101");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "ANDI" :
                    in.setOpcode("01110");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "OR" :
                    in.setOpcode("01111");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "ORI" :
                    in.setOpcode("10000");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "XOR" :
                    in.setOpcode("10001");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "XORI" :
                    in.setOpcode("10010");
                    in.setInType(Instruction.instType.I_TYPE);
                    break;
                case "NOT" :
                    in.setOpcode("10011");
                    in.setSel("0000");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "BIC" :
                    in.setOpcode("10100");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "LDA" :
                    in.setOpcode("10101");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    break;
                case "LDC" :
                    in.setOpcode("10110");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    break;
                case "LDO" :
                    in.setOpcode("10111");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "STR" :
                    in.setOpcode("11000");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    break;
                case "STO" :
                    in.setOpcode("11001");
                    in.setInType(Instruction.instType.R_TYPE);
                    break;
                case "B" :
                    in.setOpcode("11010");
                    in.setInType(Instruction.instType.J_TYPE);
                    break;
                case "BR" :
                    in.setOpcode("11011");
                    in.setSel("0000");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "CALL" :
                    in.setOpcode("11100");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    break;
                case "RET" :
                    in.setOpcode("11101");
                    in.setImm("00000000000");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    return in;
                case "PUSH" :
                    in.setOpcode("11110");
                    in.setSel("0000");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "POP" :
                    in.setOpcode("11110");
                    in.setSel("0001");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "INC" :
                    in.setOpcode("11110");
                    in.setSel("0010");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "DEC" :
                    in.setOpcode("11110");
                    in.setSel("1000");
                    in.setInType(Instruction.instType.SINGLE_OP);
                    break;
                case "SYSCALL" :
                    in.setOpcode("11111");
                    in.setInType(Instruction.instType.SINGLE_CONST);
                    break;
            }

        }

        while(Character.isWhitespace(charBuff))
        {
            charBuff = getChar();
        }

        if(in.getInType().equals(Instruction.instType.R_TYPE))
        {
            String rs = "";
            String rt = "";
            do{
                rs += charBuff;
                charBuff = getChar();
            }while(Character.isLetterOrDigit(charBuff));
            in.setRs(in.getRegs().get(rs));

            charBuff = getChar(); //for the comma
            while(Character.isWhitespace(charBuff))
            {
                charBuff = getChar();
            }


            do{
                rt += charBuff;
                charBuff = getChar();
            }while(Character.isLetterOrDigit(charBuff));
            in.setRt(in.getRegs().get(rt));
        }



        else if(in.getInType().equals(Instruction.instType.I_TYPE))
        {
            String rs = "";
            String immediate = "";
            do{
                rs += charBuff;
                charBuff = getChar();
            }while(Character.isLetterOrDigit(charBuff));
            in.setRs(in.getRegs().get(rs));

            charBuff = getChar(); //for the comma
            while(Character.isWhitespace(charBuff))
            {
                charBuff = getChar();
            }

            do{
                immediate += charBuff;
                charBuff = getChar();
            }while(Character.isDigit(charBuff));
            in.setImm(immediate);

        }
        else if(in.getInType().equals(Instruction.instType.J_TYPE))
        {
            String label = "";
            do{
                label += charBuff;
                charBuff = getChar();
            }while(Character.isDigit(charBuff));
            in.setImm(label);

        }
        else if(in.getInType().equals(Instruction.instType.SHIFT))
        {
            String rs = "";
            String immediate = "";
            do{
                rs += charBuff;
                charBuff = getChar();
            }while(Character.isLetterOrDigit(charBuff));
            in.setRs(in.getRegs().get(rs));

            charBuff = getChar(); //for the comma
            while(Character.isWhitespace(charBuff))
            {
                charBuff = getChar();
            }

            do{
                immediate += charBuff;
                charBuff = getChar();
            }while(Character.isDigit(charBuff));
            in.setImm(immediate);
        }
        else if(in.getInType().equals(Instruction.instType.SINGLE_CONST))
        {
            String val = "";
            do{
                val += charBuff;
                charBuff = getChar();
            }while(Character.isDigit(charBuff));
            in.setImm(val);
        }
        else if(in.getInType().equals(Instruction.instType.SINGLE_OP))
        {
            String rs = "";
            do{
                rs += charBuff;
                charBuff = getChar();
            }while(Character.isLetterOrDigit(charBuff));
            in.setRs(in.getRegs().get(rs));
        }
        return in;
    }

    public List<Instruction> getInstructions()
    {
        List<Instruction> insts = new ArrayList<>();
        while(insts.size() < instructions.size())
        {
            Instruction ins = getInstruction();
            if (ins)
            {
                insts.add(getInstruction());
                pc += 2;
            }
        }

        return insts;
    }


}




















