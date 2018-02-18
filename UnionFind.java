
public class UnionFind{
	public static void main(String[] args){
		UnionFind uf = new UnionFind(10);
		uf.union(1, 2);
		uf.union(0, 1);
		System.out.println(uf.find(0) == uf.find(3));
	}
	
	int rank[], parent[];
	
	UnionFind(int size){
		rank = new int[size];
		parent = new int[size];
		for(int i = 0; i < size; i++){
			parent[i] = i;
		}
	}
	
	void union(int a, int b){
		int aRoot = find(a);
		int bRoot = find(b);
		if(rank[aRoot] > rank[bRoot])
			parent[bRoot] = aRoot;
		else if(rank[bRoot] > rank[aRoot])
			parent[aRoot] = bRoot;
		else{
			parent[bRoot] = aRoot;
			rank[aRoot]++;
		}
	}
	
	int find(int a){
		if(parent[a] != a)
			parent[a] = find(parent[a]);
		return parent[a];
	}
}
