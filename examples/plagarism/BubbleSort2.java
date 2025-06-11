public class OrdenarBurbuja {
    public static void main(String[] args) {
        int[] numeros = {64, 34, 25, 12, 22, 11, 90};
        ordenar(numeros);
        System.out.println("Array ordenado: ");
        for(int i = 0; i < numeros.length; i++) {
            System.out.print(numeros[i] + " ");
        }
    }
    static void ordenar(int[] numeros) {
        int n = numeros.length;
        for (int i = 0; i < n-1; i++)
            for (int j = 0; j < n-i-1; j++)
                if (numeros[j] > numeros[j+1]) {
                    int temp = numeros[j];
                    numeros[j] = numeros[j+1];
                    numeros[j+1] = temp;
                }
    }
}
