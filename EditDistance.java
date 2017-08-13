public class EditDistance{
	public static void editDistance(String s1, String s2){
		int[][] dp = new int[s1.length() + 1][s2.length() + 1];
		
		for(int i = 0; i <= s1.length(); i++){
			dp[i][0] = i;
		}
		for(int i = 0; i <= s2.length(); i++){
			dp[0][i] = i;
		}
		
		for(int i = 1; i <= s1.length(); i++){
			for(int j = 1; j <= s2.length(); j++){
				if(s1.charAt(i - 1) == s2.charAt(j - 1))
					dp[i][j] = dp[i - 1][j - 1];
				else
					dp[i][j] = Math.min(Math.min(dp[i][j - 1], dp[i - 1][j]), dp[i - 1][j - 1]) + 1;
			}
		}
		System.out.println(dp[s1.length()][s2.length()]);
	}
	
	public static void search(String s1, String s2){
		int[][] dp = new int[s1.length() + 1][s2.length() + 1];
		
		for(int i = 0; i <= s1.length(); i++){
			dp[i][0] = 0;
		}
		for(int i = 0; i <= s2.length(); i++){
			dp[0][i] = i;
		}
		
		for(int i = 1; i <= s1.length(); i++){
			for(int j = 1; j <= s2.length(); j++){
				if(s1.charAt(i - 1) == s2.charAt(j - 1))
					dp[i][j] = dp[i - 1][j - 1];
				else
					dp[i][j] = Math.min(Math.min(dp[i][j - 1], dp[i - 1][j]), dp[i - 1][j - 1]) + 1;
			}
		}
		
		int min = Integer.MAX_VALUE;
		for(int i = 0; i <= s1.length(); i++){
			min = Math.min(min, dp[i][s2.length()]);
		}
		
		System.out.println(min);
	}
	
	public static void editDistance2(String s1, String s2){
		if(s1.length() > s2.length()){
			String temp = s1;
			s1 = s2;
			s2 = temp;
		}
		
		int[] curr = new int[s1.length() + 1];
		int[] prev = new int[s1.length() + 1];
		
		for(int i = 1; i <= s2.length(); i++){
			curr[0] = i;
			for(int j = 1; j <= s1.length(); j++){
				if(s2.charAt(i - 1) == s1.charAt(j - 1))
					curr[j] = i == 1 ? j - 1 : prev[j - 1];
				else
					curr[j] = Math.min(Math.min(i == 1 ? j : prev[j], curr[j - 1]), i == 1 ? j - 1 : prev[j - 1]) + 1;
				if(i < s2.length())
					prev[j - 1] = curr[j - 1];
			}
			if(i < s2.length())
				prev[s1.length()] = curr[s1.length()];
		}
		
		System.out.println(curr[s1.length()]);
	}
	
	public static void main(String[] args){
		editDistance("abcde", "bcd");
		editDistance2("abcde", "bcd");
		search("abcde", "bcd");
	}
}
