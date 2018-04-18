public class Greet {
    public static void main(String[] args) {
        System.out.println("Wie heißt du, Fremder?");
        String name = System.console().readLine();
        System.out.println("Hallo, " + name + "!");
    }
}