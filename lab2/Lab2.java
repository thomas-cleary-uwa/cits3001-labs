package lab2;


public class Lab2 {

    // main
    public static void main(String[] args) {
        Lab2.fiveTest();
    }


    public static void triangleTest() {
        // adjacency matrix for points
        // (1, 1), (1, 2), (2, 1)
        double[][] adjacencyMatrix = new double[][]{
            {0, 1, 1},
            {1, 0, 2},
            {1, 2, 0}
        };

        nn2optTest(adjacencyMatrix);
    }


    public static void fiveTest() {
        double[][] adjMatrix = new double[][] {
            {0, 3, 3, 3, 3},
            {3, 0, 3, 3, 3},
            {3, 3, 0, 3, 3},
            {3, 3, 3, 0, 3},
            {3, 3, 3, 3, 0}
        };

        nn2optTest(adjMatrix);
    }


    public static void nn2optTest(double[][] adjMatrix) {
        int[] path = tspnn(adjMatrix);

        int[] bestPath = tsp2opt(path, adjMatrix);

        printPath(
            bestPath, 
            getPathDistance(bestPath, adjMatrix), 
            "Best Path Found"
        );
    }


    public static void printPath(int[] path, int cost, String heading) {
        System.out.println(heading);
        System.out.println("Cost: " + cost);
        for (int i = 0; i < path.length; i++) {
            System.out.println(path[i]);
        }
    }


    /**
     * Returns the shortest tour found by exercising the NN algorithm 
     * from each possible starting city in table.
     * table[i][j] == table[j][i] gives the cost of travel between City i and 
     * City j.
     */
    public static int[] tspnn(double[][] table)
    {
        int numCities = table[0].length;

        // initialise best path and its cost
        int[] bestPath   = new int[numCities];
        double bestPathCost = -1.0; // negative so we know first path is better

        // find the NN path for this city
        for (int city = 0; city < numCities; city++) {
            // initialise array for this cities best path
            int[] path = new int[numCities];
            path[0] = city;

            boolean[] visited = new boolean[numCities];
            visited[city] = true;

            int numVisited      = 1;
            int currentLocation = city;
            double pathCost = 0;
            
            // while we have more cities to visit, get the next closest city
            // relative to the previous city visited
            while (numVisited < numCities) {
                double[] distances      = table[currentLocation];
                double   shortest       = -1.0;
                int      shortestIndex  = -1;

                // for each distance
                for (int i  = 0; i < numCities; i++) {
                    // if we have not already been to this city
                    if (!visited[i]) {
                        double distance = distances[i];

                        if ((shortest < 0 && shortestIndex < 0) ||
                            (distance < shortest)) {

                            shortest      = distances[i];
                            shortestIndex = i;
                        }
                    }
                }
                path[numVisited] = shortestIndex;
                currentLocation  = shortestIndex;
                visited[shortestIndex] = true;
                pathCost += shortest;
                numVisited++;
            }

            // add distance from last to first city
            pathCost += table[city][path[path.length-1]];

            if (bestPathCost < 0 || pathCost < bestPathCost) {
                bestPath = path;
                bestPathCost = pathCost;
            }
        }
        return bestPath;
    }

    /**
    * Uses 2-OPT repeatedly to improve cs, choosing the shortest option in each
    * iteration.
    * You can assume that cs is a valid tour initially.
    * table[i][j] == table[j][i] gives the cost of travel between City i and 
    * City j.
    */
    public static int[] tsp2opt(int[] cs, double[][] table)
    {
        int[] bestPath   = cs;
        int bestDistance =  getPathDistance(bestPath, table);

        int numCities = cs.length;

        boolean searchExhausted = false;

        // while we have not performed all swaps on the current best path      
        while (!searchExhausted) {
            // for each city
            for (int i = 0; i < numCities - 1; i++) {
                boolean newBest = false;
                // perform swap with each of the other cities
                for (int k = i + 1; k <= numCities - 1; k++) {
                    int[] newPath = twoOptSwap(bestPath, i, k);
                    int newDistance = getPathDistance(newPath, table);

                    if (newDistance < bestDistance) {
                        bestPath = newPath;
                        bestDistance = newDistance;
                        newBest = true;
                        break;
                    }
                }

                if (newBest) {
                    // start nested for loop cycle again on the new bestPath
                    // until we exhaust the search or find a better path and 
                    // start again
                    break;
                }
                if (i == numCities - 2) {
                    // the outer for loop reached its limit and did not find 
                    // a new best
                    searchExhausted = true;
                }
            }
        }

        return bestPath;
    }

    /**
    * Return the distance this path would take to travel
    */
    private static int getPathDistance(int[] path, double[][] distances) {
        // implement distance calculation here
        int startingCity = path[0];
        int previousCity = startingCity;

        int totalDistance = 0;


        for (int i = 1; i < path.length; i++) {
            totalDistance += distances[previousCity][path[i]];
            previousCity = path[i];
        }

        // add distance from last city visited back to the start
        totalDistance += distances[startingCity][previousCity];

        return totalDistance;
    }


    /**
     * Return path but swapped as specified by 2-opt swap operation 
     * respective to i and k
     */
    private static int[] twoOptSwap(int[] path, int i, int k) {

        int[] swappedPath = new int[path.length];

        // add 0 -> i-1 to swapped path
        for (int x = 0; x <= i - 1; x++) {
            swappedPath[x] = path[x];
        }


        // add the reverse of path[i:k+1] to swappedPath
        for (int x = i, y = k; y >= i; y--, x++) {
            swappedPath[x] = path[y];
        }

        // add path[k+1: ] back to the end of the path
        for (int z = k + 1; z < path.length; z++) {
            swappedPath[z] = path[z];
        }

        return swappedPath;
    }

}