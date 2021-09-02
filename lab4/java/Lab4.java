package lab4.java;

import java.util.*;

public class Lab4 {

    public static void main(String[] args) {
        Lab4.test();
    }


    public static void test() {
        String[] dictionary = new String[] {"AIM", "ARM", "ART", "RIM", "RAM", "RAT", "ROT", "RUM", "RUN", "BOT", "JAM", "JOB", "JAB", "LAB", "LOB", "LOG", "SUN"};

        String[] solution = Lab4.findPath(dictionary, "AIM", "BOT");

        for (String word : solution) {
            System.out.println(word);
        }
    }


    /**
     * Finds a shortest sequence of words in the dictionary such that the first word is the startWord, 
    * the last word is the endWord, and each word is equal to the previous word with one letter changed.
    * All words in the sequence are the same length. If no sequence is possible, an empty array is returned.
    * It is assumed that both startWord and endWord are elements of the dictionary.
    * @param dictionary The set of words that can be used in the sequence; all words in the dictionary are capitalised.
    * @param startWord the first word on the sequence.
    * @param endWord the last word in the sequence.
    * @return an array containing a shortest sequence from startWord to endWord, in order, 
    * using only words from the dictionary that differ by a single character.
    * */
    public static String[] findPath(String[] dictionary, String startWord, String endWord){

        // convert dictionary to a set
        Set<String> dictSet = new HashSet<String>(Arrays.asList(dictionary));

        // Keep track of neighbours found for each node we visit
        HashMap<String, ArrayList<String>> nodeNeighbours = new HashMap<String, ArrayList<String>>();

        // Keep track of how far away a node is from the start word
        HashMap<String, Integer> distances = new HashMap<String, Integer>();

        // List to store our solution in 
        ArrayList<String> solution = new ArrayList<String>();


        // Perform a BFS to get nodes and their distances from START. 
        // Do this until we find the end node.

        // add each word in dict to our node neighbours map
        for (String node : dictSet) {
            nodeNeighbours.put(node, new ArrayList<String>());
        }

        Queue<String> queue = new LinkedList<String>();
        queue.offer(startWord);
        distances.put(startWord, 0);


        while (!queue.isEmpty()) {
            int count = queue.size();
            boolean foundEnd = false;

            for (int i = 0; i < count; i++) {
                String currNode = queue.poll();

                int currNodeDist = distances.get(currNode);

                ArrayList<String> currNodeNeighbours = getNeighbours(currNode, dictSet);

                for (String neighbour : currNodeNeighbours) {
                    nodeNeighbours.get(currNode).add(neighbour);

                    if (!distances.containsKey(neighbour)) {
                        distances.put(neighbour, currNodeDist + 1);

                        if (!endWord.equals(neighbour)) {
                            queue.offer(neighbour);
                        }
                        else {
                            foundEnd = true;
                            break;
                        }
                    }
                }
                if (foundEnd) {break;}
            }
            if (foundEnd) {break;}
        }

        // if no path found return an empty array
        if (!distances.containsKey(endWord)) {
            return new String[0];
        }

        getPath(startWord, endWord, nodeNeighbours, distances, solution);


        return solution.toArray(new String[0]);
    }


    private static boolean getPath(String currNode, 
                                String endNode, 
                                HashMap<String, ArrayList<String>> nodeNeighbours, 
                                HashMap<String, Integer> distances,
                                ArrayList<String> solution) 
    {
        int solutionDist = distances.get(endNode) + 1;

        solution.add(currNode);

        if (solution.size() == solutionDist) {
            if (currNode.equals(endNode)) {
                return true;
            }
            else {
                return false;
            }
        }

        for (String neighbour : nodeNeighbours.get(currNode)) {
            if (distances.get(currNode) + 1 == distances.get(neighbour)) {
                if (!getPath(neighbour, endNode, nodeNeighbours, distances, solution)) {
                    solution.remove(solution.size()-1);
                }
                else {
                    return true;
                }
            }
        }
        return false; // this should never happen
    }


    private static ArrayList<String> getNeighbours(String node, Set<String> dict) {
        ArrayList<String> neighbours  = new ArrayList<String>();
        char[] node_chars = node.toCharArray();

        for (char ch = 'A'; ch <= 'Z'; ch++) {
            for (int i = 0; i < node_chars.length; i++) {
                if (node_chars[i] != ch) {
                    char old_ch = node_chars[i]; // save old char to put back after checking dict
                    node_chars[i] = ch;
                    if (dict.contains(String.valueOf(node_chars))) {
                        neighbours.add(String.valueOf(node_chars));
                    }
                    node_chars[i] = old_ch;
                }
            }
        }
        return neighbours;
    }
}