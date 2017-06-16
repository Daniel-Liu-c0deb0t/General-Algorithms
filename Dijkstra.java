package reference;

import java.util.*;

public class Dijkstra {
		
	public static ArrayList<Node> findShortestPath(Node[] nodes, Edge[] edges, Node target) {
		int[][] Weight = initializeWeight(nodes, edges);
		int[] D = new int[nodes.length];
		Node[] P = new Node[nodes.length];
		ArrayList<Node> C = new ArrayList<Node>();
		
		// (C)andidate set,
		// (D)ijkstra special path length
		// (P)revious Node along shortest path
		for(int i=0; i<nodes.length; i++){
			C.add(nodes[i]);
			D[i] = Weight[0][i];
			if(D[i] != Integer.MAX_VALUE){
				P[i] = nodes[0];
			}
		}

		for(int i = 0; i < nodes.length-1; i++){
			int l = Integer.MAX_VALUE;
			Node n = nodes[0];
			for(Node j : C){
				if(D[j.name] < l){
					n = j;
					l = D[j.name];
				}
			}
			C.remove(n);
			
			for(int j=0; j<nodes.length-1; j++){
				if(D[n.name] != Integer.MAX_VALUE && Weight[n.name][j] != Integer.MAX_VALUE && D[n.name] + Weight[n.name][j] < D[j]){
					D[j] = D[n.name] + Weight[n.name][j];
					P[j] = n;
				}
			}
		}
		C.clear();
		int loc = target.name;
		C.add(target);
		while(P[loc] != nodes[0]){
			if(P[loc] == null){
				return null;
			}
			C.add(0, P[loc]);
			loc = P[loc].name;
		}
		C.add(0, nodes[0]);
		return C;
	}

	private static int[][] initializeWeight(Node[] nodes, Edge[] edges){
		int[][] Weight = new int[nodes.length][nodes.length];
		for(int i=0; i<nodes.length; i++){
			Arrays.fill(Weight[i], Integer.MAX_VALUE);
		}
		for(Edge e : edges){
			Weight[e.from.name][e.to.name] = e.weight;
		}
		return Weight;
	}
	
	private static class Node{
		int name;
		
		public Node(int name){
			this.name = name;
		}
	}
	
	private static class Edge{
		Node from, to;
		int weight;
		
		public Edge(Node from, Node to, int weight){
			this.weight = weight;
		}
	}
}