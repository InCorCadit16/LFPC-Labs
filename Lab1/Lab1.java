import java.util.*;

public class Lab1 {
    
    static List<String> N = List.of("S", "B", "L");
    static List<String> T = List.of("a", "b", "c");

    public static void main(String[] args) {
        String input = "S->aB;B->bB;B->cL;L->cL;L->aS;L->b";
        printCheck("abcaac");
    }

    public static void printCheck(String s) {
        System.out.printf("%s: %s", s, check(s) ? "Approved" : "Rejected");
    }

    public static boolean check(String s) {
        char state = 'S';
        for (char c : s.toCharArray()) {
            switch (c) {
                case 'a':
                    if (state == 'S') state = 'B';
                    else if (state == 'L') state = 'S';
                    else return false;
                    break;
                case 'b':
                    if (state == 'B') state = 'B';
                    else return false;
                    break;
                case 'c':
                    if (state == 'B' || state == 'L') state = 'L'; 
                    else return false;
                    break;
                default:
                    return false;
            }
        }

        return state == 'L';
    }
    
}
