
public class BIT{
	int[] bit;
	
	public static void main(String[] args){
		//point update, range query
		BIT t = new BIT(5);
		t.update(0, 1);
		t.update(1, 2);
		System.out.println(t.query(1) - t.query(1 - 1));
		
		//range update, point query
		BIT t2 = new BIT(5);
		t2.update(0, 3); //left
		t2.update(3 + 1, -3); //right
		System.out.println(t2.query(3));
		
		BIT t3 = new BIT(6);
		t3.update(0, 1);
		t3.update(2, 2);
		t3.update(3, 1);
		t3.update(5, 1);
		//if first index is filled then result = 0
		System.out.println(t3.floor(1)); //leftmost index where prefix sum = 1
		System.out.println(t3.ceil(1)); //rightmost index where prefix sum = 1
	}
	
	BIT(int n){
		bit = new int[n + 1];
	}
	
	int query(int i){
		i++;
		int res = 0;
		while(i > 0){
			res += bit[i];
			i -= i & (-i);
		}
		return res;
	}
	
	void update(int i, int val){
		i++;
		while(i < bit.length){
			bit[i] += val;
			i += i & (-i);
		}
	}
	
	int floor(int val){
		int sum = 0;
		int res = 0;
		int max = Integer.numberOfTrailingZeros(Integer.highestOneBit(bit.length - 1));
		for(int i = 1 << max; i > 0 && res + i < bit.length; i >>= 1){
			if(sum + bit[res + i] < val){
				sum += bit[res + i];
				res += i;
			}
		}
		return res;
	}
	
	int ceil(int val){
		int res = 0;
		int max = Integer.numberOfTrailingZeros(Integer.highestOneBit(bit.length - 1));
		for(int i = max; i >= 0; i--){
			int p = res + (1 << i);
			if(p < bit.length && bit[p] <= val){
				val -= bit[p];
				res += 1 << i;
			}
		}
		return res - 1;
	}
}
