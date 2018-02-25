import java.util.ArrayList;
import java.util.Arrays;

public class EulerTourAndLCA{
	static ArrayList<Integer>[] g;
	
	public static void main(String[] args){
		g = new ArrayList[6];
		g[0] = new ArrayList<Integer>(Arrays.asList(1, 4));
		g[1] = new ArrayList<Integer>(Arrays.asList(2, 3));
		g[2] = new ArrayList<Integer>(Arrays.asList());
		g[3] = new ArrayList<Integer>(Arrays.asList(5));
		g[4] = new ArrayList<Integer>(Arrays.asList());
		g[5] = new ArrayList<Integer>(Arrays.asList());
		
		calcSubtree(0);
		System.out.println(Arrays.toString(pos));
		System.out.println(Arrays.toString(left));
		System.out.println(Arrays.toString(right));
		
		calcPath(0); //used to calculate LCA
		System.out.println(Arrays.toString(pos));
		System.out.println(Arrays.toString(left));
		System.out.println(Arrays.toString(right));
		
		int l = 2, r = 5;
		System.out.println(lca(l, r));
	}
	
	static int idx;
	static int[] pos, left, right;
	static void calcSubtree(int root){
		idx = 0;
		pos = new int[g.length];
		left = new int[g.length];
		right = new int[g.length];
		dfs1(root, -1);
	}
	
	static void dfs1(int u, int p){
		pos[u] = idx;
		left[u] = idx;
		right[u] = idx++;
		for(int v : g[u]){
			if(v == p) continue;
			dfs1(v, u);
			right[u] = Math.max(right[u], right[v]);
		}
	}
	
	static int[] lvl;
	static int[][] dp;
	static int num = 31; //log of n
	static void calcPath(int root){
//		idx = 0;
//		pos = new int[g.length];
//		left = new int[g.length];
//		right = new int[g.length];
		lvl = new int[g.length];
		dp = new int[num][g.length];
		dp[0][root] = 0;
		dfs2(root, -1);
	}
	
	static void dfs2(int u, int p){
//		pos[u] = idx;
//		left[u] = idx++;
		for(int i = 1; i < num; i++){
			dp[i][u] = dp[i - 1][dp[i - 1][u]];
		}
		for(int v : g[u]){
			if(v == p) continue;
			lvl[v] = lvl[u] + 1;
			dp[0][v] = u;
			dfs2(v, u);
		}
//		right[u] = idx++;
	}
	
	static int lca(int u, int v){
		if(lvl[u] > lvl[v]){
			int temp = u;
			u = v;
			v = temp;
		}
		for(int i = num - 1; i >= 0; i--){
			if(lvl[v] - (1 << i) >= lvl[u])
				v = dp[i][v];
		}
		if(u == v)
			return u;
		for(int i = num - 1; i >= 0; i--){
			if(dp[i][u] != dp[i][v]){
				u = dp[i][u];
				v = dp[i][v];
			}
		}
		return dp[0][u];
	}
}
