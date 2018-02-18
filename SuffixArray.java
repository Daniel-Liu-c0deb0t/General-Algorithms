
public class SuffixArray{
	Suffix[] sa;
	int[] lcp;
	
	public static void main(String[] args){
		String str = "aabbcdaaccb`";
		SuffixArray s = new SuffixArray(str);
		for(int i = 0; i < str.length(); i++){
			System.out.println(str.substring(s.getSA(i)));
			System.out.println(s.getLCP(i));
		}
	}
	
	SuffixArray(String s){
		sa = new Suffix[s.length()];
		for(int i = 0; i < s.length(); i++){
			sa[i] = new Suffix(i, s.charAt(i) - 'a' + 1, i + 1 < s.length() ? s.charAt(i + 1) - 'a' + 1 : 0);
		}
		
		radixSort();
		
		int[] idx = new int[s.length()];
		for(int i = 4; i < s.length() * 2; i *= 2){
			int rank = 1;
			int prevRank = sa[0].rank1;
			sa[0].rank1 = rank;
			idx[sa[0].idx] = 0;
			
			for(int j = 1; j < s.length(); j++){
				if(sa[j].rank1 == prevRank && sa[j].rank2 == sa[j - 1].rank2){
					prevRank = sa[j].rank1;
					sa[j].rank1 = rank;
				}else{
					prevRank = sa[j].rank1;
					sa[j].rank1 = ++rank;
				}
				idx[sa[j].idx] = j;
			}
			for(int j = 0; j < s.length(); j++){
				int next = sa[j].idx + i / 2;
				sa[j].rank2 = next < s.length() ? sa[idx[next]].rank1 : 0;
			}
			
			radixSort();
		}
		
		lcp = new int[s.length()];
		
		int[] inv = new int[s.length()];
		for(int i = 0; i < s.length(); i++)
			inv[getSA(i)] = i;
		
		int prev = 0;
		for(int i = 0; i < s.length(); i++){
			if(inv[i] == s.length() - 1){
				prev = 0;
				continue;
			}
			int j = getSA(inv[i] + 1);
			while(i + prev < s.length() && j + prev < s.length() && s.charAt(i + prev) == s.charAt(j + prev))
				prev++;
			lcp[inv[i]] = prev;
			if(prev > 0)
				prev--;
		}
	}
	
	int getSA(int i){
		return sa[i].idx;
	}
	
	int getLCP(int i){
		return lcp[i];
	}
	
	void radixSort(){
		int max = 0;
		for(int i = 0; i < sa.length; i++){
			max = Math.max(max, sa[i].rank1 * 100 + sa[i].rank2);
		}
		
		for(int i = 1; max / i > 0; i *= 10){
			countingSort(i);
		}
	}
	
	void countingSort(int div){
		Suffix[] res = new Suffix[sa.length];
		int[] count = new int[10];
		
		for(int i = 0; i < sa.length; i++){
			int n = sa[i].rank1 * 100 + sa[i].rank2;
			count[(n / div) % 10]++;
		}
		
		for(int i = 1; i < 10; i++){
			count[i] += count[i - 1];
		}
		
		for(int i = sa.length - 1; i >= 0; i--){
			int n = sa[i].rank1 * 100 + sa[i].rank2;
			res[--count[(n / div) % 10]] = sa[i];
		}
		
		for(int i = 0; i < sa.length; i++){
			sa[i] = res[i];
		}
	}
	
	class Suffix{
		int idx, rank1, rank2;
		
		public Suffix(int idx, int rank1, int rank2){
			this.idx = idx;
			this.rank1 = rank1;
			this.rank2 = rank2;
		}
	}
}
