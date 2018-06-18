
public class SqrtDecomposition{
	static int numBlocks = 100;
	static int n = 10000;
	static int blockSize = n % numBlocks == 0 ? n / numBlocks : n / numBlocks + 1;
	static BIT[] b = new BIT[numBlocks]; //only updated for border blocks
	static int[] lazy = new int[numBlocks]; //per element update for non-border blocks
	static int[] sum = new int[numBlocks]; //sum of a block
	
	public static void main(String[] args){
		for(int i = 0; i < b.length; i++)
			b[i] = new BIT(blockSize);
		update(0, 2000, 1);
		update(1000, 4000, 1);
		for(int i = 0; i < n; i++){
			System.out.println(query(i, i));
		}
		System.out.println(query(0, n - 1));
	}
	
	static int query(int l, int r){
		int res = 0;
		if(l % blockSize != 0){
			//calc length while making sure l and r can be on the same block
			int length = Math.min(blockSize - 1, r / blockSize != l / blockSize ?
					Integer.MAX_VALUE : r % blockSize) - l % blockSize + 1;
			res += b[l / blockSize].query(Math.min(blockSize - 1, r / blockSize != l / blockSize ?
					Integer.MAX_VALUE : r % blockSize)) - b[l / blockSize].query(l % blockSize - 1);
			res += lazy[l / blockSize] * length;
			l = (l / blockSize + 1) * blockSize;
		}
		if(l / blockSize > r / blockSize) //early return if l and r are in the same block
			return res;
		if(r % blockSize != blockSize - 1){
			int length = r % blockSize + 1;
			res += b[r / blockSize].query(r % blockSize);
			res += lazy[r / blockSize] * length;
			r = (r / blockSize - 1) * blockSize;
		}
		for(int i = l / blockSize; i <= r / blockSize; i++){
			res += sum[i];
		}
		return res;
	}
	
	static void update(int l, int r, int val){
		if(l % blockSize != 0){
			for(int i = l % blockSize; i < blockSize &&
					(r / blockSize != l / blockSize || i <= r % blockSize); i++){
				b[l / blockSize].update(i, val);
				sum[l / blockSize] += val;
			}
			l = (l / blockSize + 1) * blockSize;
		}
		if(l / blockSize > r / blockSize) //early return if l and r are in the same block
			return;
		if(r % blockSize != blockSize - 1){
			for(int i = r % blockSize; i >= 0; i--){
				b[r / blockSize].update(i, val);
				sum[r / blockSize] += val;
			}
			r = (r / blockSize - 1) * blockSize;
		}
		for(int i = l / blockSize; i <= r / blockSize; i++){
			sum[i] += val * blockSize;
			lazy[i] += val;
		}
	}
}
