package reference;

import java.util.*;

public class Knapsack {
	public static void main(String[] args){
		int[][] dp1 = new int[3][4];
		
		for(int i = 0; i < dp1.length; i++){
			for(int j = 0; j < dp1[0].length; j++){
				dp1[i][j] = -1;
			}
		}
		
		System.out.println(knapsack01(2, 3, 0, new int[]{1, 2, 3}, new int[]{1, 2, 4}, dp1));
		
		int[] dp2 = new int[4];
		
		Arrays.fill(dp2, -1);
		
		System.out.println(knapsackUnbounded(3, new int[]{1, 2, 3}, new int[]{3, 2, 1}, dp2));
	}
	
	public static int knapsackUnbounded(int w, int[] weights, int[] values, int[] dp){
		if(dp[w] != -1)
			return dp[w];
		
		int max = 0;
		
		for(int i = 0; i < weights.length; i++){
			if(weights[i] <= w)
				max = Math.max(max, values[i] + knapsackUnbounded(w - weights[i], weights, values, dp));
		}
		
		dp[w] = max;
		
		return dp[w];
	}
	
	public static int knapsack01(int i, int w, int v, int[] weights, int[] values, int[][] dp){
		if(i < 0)
			return v;
		
		if(dp[i][w] != -1)
			return dp[i][w];
		
		if(w < weights[i])
			dp[i][w] = knapsack01(i - 1, w, v, weights, values, dp);
		else
			dp[i][w] = Math.max(knapsack01(i - 1, w, v, weights, values, dp),  knapsack01(i - 1, w - weights[i], v + values[i], weights, values, dp));
		
		return dp[i][w];
	}
}
