import java.util.Arrays;
import java.util.HashMap;

public class Dinics{
	public static void main(String[] args) throws Exception{
		g = new HashMap[4];
		for(int i = 0; i < g.length; i++)
			g[i] = new HashMap<Integer, Integer>();
		g[0].put(1, 1);
		g[0].put(2, 2);
		g[1].put(3, 1);
		g[2].put(3, 2);
		
		System.out.println(dinic(0, 3));
	}
	
	static int[] level;
	static HashMap<Integer, Integer>[] g;
	static int dinic(int s, int t){
		level = new int[g.length];
		int res = 0;
		while(bfs(s, t)){
			int temp = 0;
			while((temp = dfs(s, 1000000000, t)) != 0)
				res += temp;
		}
		return res;
	}
	
	static boolean bfs(int s, int t){
		Arrays.fill(level, 0);
		level[s] = 1;
		int[] q = new int[g.length * 2];
		int l = 0, r = 0;
		q[r++] = s;
		while(l != r){
			int x = q[l++];
			if(x == t)
				return true;
			for(int v : g[x].keySet()){
				if(g[x].get(v) == 0)
					continue;
				if(level[v] == 0){
					level[v] = level[x] + 1;
					q[r++] = v;
				}
			}
		}
		return false;
	}
	
	static int dfs(int u, int maxF, int t){
		if(u == t)
			return maxF;
		int res = 0;
		for(int v : g[u].keySet()){
			if(level[u] + 1 == level[v]){
				int min = Math.min(maxF - res, g[u].get(v));
				int f = dfs(v, min, t);
				g[u].put(v, g[u].get(v) - f);
				g[v].put(u, g[v].getOrDefault(u, 0) + f);
				res += f;
				if(res == maxF)
					return res;
			}
		}
		return res;
	}
}
