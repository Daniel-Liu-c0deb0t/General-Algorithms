import java.util.Arrays;
import java.util.HashMap;

public class MinCostMaxFlow{
	public static void main(String[] args){
		g = new HashMap[4];
		for(int i = 0; i < g.length; i++)
			g[i] = new HashMap<Integer, int[]>();
		g[0].put(1, new int[]{1, 1}); //{flow, cost}
		g[1].put(0, new int[]{0, -1});
		
		g[0].put(2, new int[]{2, 2});
		g[2].put(0, new int[]{0, -2});
		
		g[1].put(3, new int[]{1, 3});
		g[3].put(1, new int[]{0, -3});
		
		g[2].put(3, new int[]{2, 1});
		g[3].put(2, new int[]{0, -1});
		
		int[] res = minCostMaxFlow(0, 3);
		System.out.println(res[0] + " " + res[1]);
	}
	
	static int[] prev;
	static int[] dist;
	static int[][] path;
	static HashMap<Integer, int[]>[] g;
	static int[] minCostMaxFlow(int s, int t){
		prev = new int[g.length];
		dist = new int[g.length];
		path = new int[g.length][2];
		
		int cost = 0;
		int flow = 0;
		while(spfa(s, t)){
			int f = 1000000000;
			for(int u = t; u != s; u = prev[u]){
				if(g[path[u][0]].get(path[u][1])[0] < f){
					f = g[path[u][0]].get(path[u][1])[0];
				}
			}
			flow += f;
			cost += dist[t] * f;
			for(int u = t; u != s; u = prev[u]){
				g[path[u][0]].get(path[u][1])[0] -= f;
				g[path[u][1]].get(path[u][0])[0] += f;
			}
		}
		return new int[]{flow, cost};
	}
	
	static boolean spfa(int s, int t){
		Arrays.fill(prev, -1);
		Arrays.fill(dist, 1000000000);
		dist[s] = 0;
		int[] q = new int[g.length * 2];
		int l = 0, r = 0;
		q[r++] = s;
		while(l != r){
			int u = q[l++];
			for(int v : g[u].keySet()){
				if(g[u].get(v)[0] == 0)
					continue;
				if(dist[u] + g[u].get(v)[1] < dist[v]){
					dist[v] = dist[u] + g[u].get(v)[1];
					prev[v] = u;
					path[v] = new int[]{u, v};
					q[r++] = v;
				}
			}
		}
		if(prev[t] == -1)
			return false;
		return true;
	}
}
