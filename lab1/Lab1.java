package lab1;

import java.util.*;


public class Lab1 {

/**
 * Apply the greedy algorithm to calculate coin change.
 * @param amount a non-negative integer which is required to be made up.
 * @param denominations the available coin types (unique positive integers)
 * @return a map of each denomination to the number of times it is used in the solution.
 * **/

    // main 
    public static void main(String[] args) {
        Lab1.question3SmallExample();
    }

    // run the lab quiz example
    public static void quizQ1Example() {
        int[] denominations = {1,2,3};
        Map<Integer, Integer> change = greedyChange(5, denominations);         

        Integer[] keys = change.keySet().toArray(new Integer[0]);
        Arrays.sort(keys);

        for (Integer i: keys) {
            System.out.println(i+":"+change.get(i));
        }
    }

    public static void quizQ3Example() {
        int[] denominations = {12,15,17,231,421,527,1};
        int amount = 2134;

        Lab1.optimalChange(amount, denominations);
    }

    public static void question3SmallExample() {
        int[] denominations = {9,6,5,1};
        int amount = 11;

        Lab1.optimalChange(amount, denominations);
    }

    // Greedy solution
    public static Map<Integer,Integer> greedyChange(int amount, int[] denominations){
        // create new HashMap and create key for each denomination with value set to 0
        Map<Integer, Integer> changeDenoms = new HashMap<Integer, Integer>();
        for (int i = 0; i < denominations.length; i++) {
            changeDenoms.put(denominations[i], 0);
        }

        // sort denominations from smallest to largest
        Arrays.sort(denominations);
        int denomIndex = denominations.length - 1;

        int amountRemaining = amount;

        // initial test of loop invariant
        assert Lab1.loopInvariant(amount, amountRemaining, changeDenoms);

        // while we still have change to make up
        while (amountRemaining > 0) {
            int denom = denominations[denomIndex];

            // if the current largest denomination is smaller than the change
            // left to give
            if (amountRemaining - denom >= 0) {
                changeDenoms.put(denom, changeDenoms.get(denom) + 1);
                amountRemaining -= denom;
            }
            else {
                // current denom amount is to large, move to next largest
                denomIndex--;
            }

            // test loop invariant at end of iteration
            assert Lab1.loopInvariant(amount, amountRemaining, changeDenoms);
        }

        // test that loop invariant still true after the end of the loop
        assert Lab1.loopInvariant(amount, amountRemaining, changeDenoms);

        return changeDenoms;
    }


    // Optimal Solution (recursive so exponential time ie NOT FAST)
    public static void optimalChange(int amount, int[] denominations) {
        // create new HashMap and create key for each denomination with value set to 0
        Map<Integer, Integer> changeDenoms = new HashMap<Integer, Integer>();
        for (int i = 0; i < denominations.length; i++) {
            changeDenoms.put(denominations[i], 0);
        }

        int minNumCoins = minCoins(denominations, amount);

        System.out.println("Min number of coins: " + minNumCoins);

    }

    // return min number of coins needed in denominations to form amount
    public static int minCoins(int[] denominations, int amount) {

        if (amount == 0 ) {
            return 0;
        }

        int minNumCoins = Integer.MAX_VALUE;

        // try each denomination
        for (int i = 0; i < denominations.length; i++) {
            if (denominations[i] <= amount) {
                int result = 1 + minCoins(denominations, amount - denominations[i]);

                // see if we can improve the current minimum found
                if (result < minNumCoins) {
                    minNumCoins = result;
                }
            }
        }
        return minNumCoins;
    }

    // assert that the invariant of a given loop is true
    public static boolean loopInvariant(int originalAmount, int amountRemaining, Map<Integer, Integer> changeGiven) {
        //add code here
        int totalChangeGiven = 0;

        for (Map.Entry<Integer, Integer> entry : changeGiven.entrySet()) {
            Integer denomination = entry.getKey();
            Integer numCoins = entry.getValue();

            totalChangeGiven += denomination * numCoins;
        }

        return (originalAmount == (amountRemaining + totalChangeGiven));
    }
}