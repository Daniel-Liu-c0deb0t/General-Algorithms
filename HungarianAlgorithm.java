import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

public class HungarianAlgorithm{
	static HashMap<Integer, Integer>[] match;
	static HashSet<Integer>[] check;
	static HashMap<Integer, ArrayList<Integer>>[] g;
	
	public static void main(String[] args){
		g = new HashMap[2];
		
		g[0] = new HashMap<Integer, ArrayList<Integer>>();
		g[1] = new HashMap<Integer, ArrayList<Integer>>();
		
		g[0].put(0, new ArrayList<Integer>(Arrays.asList(0, 1)));
		g[0].put(1, new ArrayList<Integer>(Arrays.asList(0, 1)));
		g[0].put(2, new ArrayList<Integer>(Arrays.asList(1)));
		
		g[1].put(0, new ArrayList<Integer>(Arrays.asList(0, 1)));
		g[1].put(1, new ArrayList<Integer>(Arrays.asList(0, 1, 2)));
		g[1].put(2, new ArrayList<Integer>(Arrays.asList()));
		
		System.out.println(solve());
	}
	
	static int solve(){
		match = new HashMap[2];
		check = new HashSet[2];
		
		match[0] = new HashMap<Integer, Integer>();
		match[1] = new HashMap<Integer, Integer>();
		
		check[0] = new HashSet<Integer>();
		check[1] = new HashSet<Integer>();
		
		int res = 0;
		for(int u : g[0].keySet()){
			if(!match[0].containsKey(u)){
				check[0].clear();
				check[1].clear();
				if(dfs(u, 1))
					res++;
			}
		}
		
		return res;
	}
	
	static boolean dfs(int u, int left){
		for(int v : g[left].get(u)){
			if(!check[left ^ 1].contains(v)){
				check[left ^ 1].add(v);
				if(!match[left ^ 1].containsKey(v) || dfs(v, left ^ 1)){
					match[left].put(u, v);
					match[left ^ 1].put(v, u);
					return true;
				}
			}
		}
		return false;
	}
}
