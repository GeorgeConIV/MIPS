/*EGRE 591 -- Compiler Construction
 *By Mark Johnston and George Constantine
 */

import java.io.File;
import java.io.IOException;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class FileManipulator
{
    Scanner scanner = new Scanner(System.in);
    Scanner fileScan = null;

    List<String> stringList = new ArrayList<>();

    Path inputFile;
    Path outputFile;

    String filePath;
    String pathNoFile;
    String fileName = "defaultLexerName";


    //Regex used for finding file name in file inputFile, used for file creation and consistency
    String regex = "(.+\\\\)*(.+)[.](.+)";
    Pattern nameRegex = Pattern.compile(regex);
    Matcher matcher;

    //used for loop control when invalid inputFile exists
    boolean invalidPath;

    public FileManipulator()
    {

    }

    /**
     * Initializes the file scanner, asks the user to input file path
     */
    public void initFileScanner(String filetoload)
    {
        invalidPath = false;
        //System.out.println("Enter in file inputFile of file to be compiled:");
        //filePath = scanner.next();
        //filePath = System.getProperty("user.dir")+"\\tests\\"+filetoload;
        filePath = filetoload;
        if(!(new File(filetoload)).exists())
            filePath = Paths.get(System.getProperty("user.dir"),"tests", filetoload).toString();
        System.out.println("Getting file: " + filePath);
        try
        {
            inputFile = Paths.get(filePath);
            fileScan = new Scanner(inputFile);
            //System.out.println("Loaded file");
        }
        catch (IOException e)
        {
            System.out.println("ERROR: File not found");
            System.out.println(e.getMessage());
            System.exit(1);
            invalidPath = true;
        }
    }

    public List<String> getListOfTokensWhitespaceDelimited()
    {
        while(fileScan.hasNextLine())
        {
            String toBeStored = fileScan.nextLine();
            stringList.add(toBeStored.toUpperCase());
        }

        return stringList;
    }

    /**
     * This method will create a file and write a list of strings to said file. The user can
     * either specify the path, or have the path be autogenerated
     *
     * @param inputTokens   The list of strings that will be printed to a file
     * @param writeFilePath The Optional value that allows the user to specify the path of the output file
     */
    public void writeListOfTokens(List<String> inputTokens, Optional<String> writeFilePath)
    {
        if(!writeFilePath.isPresent())
        {
            appendFileNameForLex();
            outputFile = Paths.get(pathNoFile, fileName);
            //outputFile = Paths.get(System.getProperty("user.dir")+"\\output\\"+fileName);
        }
        else
        {
            outputFile = Paths.get(writeFilePath.get());
        }

        try
        {
            Files.write(outputFile, inputTokens, StandardCharsets.UTF_8);
        }
        catch(IOException e)
        {
            e.printStackTrace();
            System.out.println("Something went wrong while writing to the text file");
        }
        //System.out.println("Tokens successfully written to " + outputFile.toString());
    }

    /**
     * This method will find the file name (without .extension) and file path using a regex
     *
     * @return fileName - the name of the file without extension
     */
    public String getFileNameFromCurrentPath()
    {
        try
        {
            matcher = nameRegex.matcher(filePath);      //grabs the file name
            matcher.find();
            fileName = matcher.group(2);
            pathNoFile = matcher.group(1);
        }
        catch(IllegalStateException e)
        {
            System.out.println("File does not follow format.");
            fileName = "defaultLexerName";
        }
        return fileName;
    }

    /**
     * Takes the current file name, and changes the extension to .lxl
     *
     * @return appended file name
     */
    public String appendFileNameForLex()
    {
        fileName = getFileNameFromCurrentPath().concat(".lxl");
        return fileName;
    }

    public Path getInputFile()
    {
        return inputFile;
    }

    public Path getOutputFile()
    {
        return outputFile;
    }

    public String getFileName()
    {
        return fileName;
    }

}