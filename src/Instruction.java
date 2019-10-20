import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Instruction
{
    public enum instType
    {
        I_TYPE, R_TYPE, J_TYPE, SHIFT, SINGLE_OP, SINGLE_CONST
    }

    static List<String> noCond = new ArrayList<>();
    static HashMap<String, String> conds = new HashMap<>();
    static HashMap<String, String> regs = new HashMap<>();
    instType inType;

    String preIn;
    String binary = "";
    String opcode;
    String rs;
    String rt;
    String cond;
    String imm;
    String type;
    String sel;
    String immBin;
    Integer pc;

    public Instruction()
    {
        initLists();
    }

    public Instruction(String preIn, Integer pc)
    {
        this.pc = pc;
        this.preIn = preIn;
        initLists();
    }

    public void initLists()
    {
        noCond.add("NOP");
        noCond.add("ADD");
        noCond.add("ADDI");
        noCond.add("SUB");
        noCond.add("SUBI");
        noCond.add("MUL");
        noCond.add("MULI");
        noCond.add("DIV");
        noCond.add("DIVI");
        noCond.add("LSL");
        noCond.add("LRS");
        noCond.add("ARS");
        noCond.add("TAR");
        noCond.add("MOV");
        noCond.add("CMP");
        noCond.add("AND");
        noCond.add("ANDI");
        noCond.add("OR");
        noCond.add("ORI");
        noCond.add("XOR");
        noCond.add("XORI");
        noCond.add("NOT");
        noCond.add("BIC");
        noCond.add("LDA");
        noCond.add("LDC");
        noCond.add("LDO");
        noCond.add("SRT");
        noCond.add("STO");
        noCond.add("B");
        noCond.add("BR");
        noCond.add("CALL");
        noCond.add("RET");
        noCond.add("PUSH");
        noCond.add("POP");
        noCond.add("INC");
        noCond.add("DEC");
        noCond.add("SYSCALL");

        conds.put("NE", "001");
        conds.put("EQ", "010");
        conds.put("LT", "011");
        conds.put("GT", "100");
        conds.put("LTE", "101");
        conds.put("GTE", "110");
        conds.put("EQZ", "111");

        regs.put("R0", "0000");
        regs.put("R1", "0001");
        regs.put("R2", "0010");
        regs.put("R3", "0011");
        regs.put("R4", "0100");
        regs.put("R5", "0101");
        regs.put("R6", "0110");
        regs.put("R7", "0111");
        regs.put("R8", "1000");
        regs.put("R9", "1001");
        regs.put("R10", "1010");
        regs.put("R11", "1011");
        regs.put("PC", "1100");
        regs.put("R12", "1100");
        regs.put("RA", "1101");
        regs.put("R13", "1110");
        regs.put("SP", "1110");
        regs.put("R14", "1110");
        regs.put("AR", "1111");
        regs.put("R15", "1111");

    }

    public HashMap<String, String> getConds()
    {
        return conds;
    }

    public HashMap<String, String> getRegs()
    {
        return regs;
    }

    public List<String> getNoCond()
    {
        return  noCond;
    }

    public instType getInType()
    {
        return inType;
    }

    public void setCond(String cond) {
        this.cond = cond;
    }

    public void setSel(String sel)
    {
        this.sel = sel;
    }

    public void setImm(String imm) {
        this.imm = imm;
    }

    public void setOpcode(String opcode) {
        this.opcode = opcode;
    }

    public void setRs(String rs) {
        this.rs = rs;
    }

    public void setRt(String rt) {
        this.rt = rt;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getBitstream()
    {
        if(inType == instType.R_TYPE)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(rs);
            binary = binary.concat(rt);
            binary = binary.concat(cond);
        }
        else if(inType == instType.I_TYPE)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(rs);
            binary = binary.concat(decimalToBin(imm));
        }
        else if(inType == instType.SINGLE_CONST)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(decimalToBin(imm));
        }
        else if(inType == instType.J_TYPE)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(decimalToBin(imm));
            binary = binary.concat(cond);
        }
        else if(inType == instType.SINGLE_OP)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(rs);
            binary = binary.concat(sel);
            binary = binary.concat(cond);

        }
        if(inType == instType.SHIFT)
        {
            binary = binary.concat(opcode);
            binary = binary.concat(rs);
            binary = binary.concat(decimalToBin(imm));
            binary = binary.concat(type);
        }

        return binary;
    }

    public String decimalToBin(String dec)
    {
        int decimal = Integer.parseInt(dec);
        String bin = Integer.toBinaryString(decimal);
        if(inType.equals(instType.I_TYPE))
        {
            if(bin.length() < 7)
            {
                int i = 0;
                String append = "";
                while((i + bin.length()) < 7) {
                    append += "0";
                    i++;
                }
                bin = append.concat(bin);
            }
            else if(bin.length() > 7)
            {
                bin = bin.substring(bin.length()-7);
            }
        }
        if(inType.equals(instType.SINGLE_CONST))
        {
            if(bin.length() < 11)
            {
                int i = 0;
                String append = "";
                while((i + bin.length()) < 11)
                {
                    append += "0";
                    i++;
                }
                bin = append.concat(bin);
            }
            else if(bin.length() > 11)
            {
                bin = bin.substring(bin.length() - 11);
            }
        }
        if(inType.equals(instType.J_TYPE))
        {
            if(bin.length() < 8)
            {
                int i = 0;
                String append = "";
                while((i + bin.length()) < 8)
                {
                    append += "0";
                    i++;
                }
                bin = append.concat(bin);
            }
            else if(bin.length() > 8)
            {
                bin = bin.substring(bin.length() - 8);
            }
        }
        if(inType.equals(instType.SHIFT))
        {
            if(bin.length() < 4)
            {
                int i = 0;
                String append = "";
                while((i + bin.length()) < 4)
                {
                    append += "0";
                    i++;
                }
                bin = append.concat(bin);
            }
            else if(bin.length() > 4)
            {
                bin = bin.substring(bin.length() - 4);
            }

        }
        return bin;
    }

    public void setInType(instType inType)
    {
        this.inType = inType;
    }
}
