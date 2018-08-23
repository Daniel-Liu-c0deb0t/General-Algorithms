import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;

public class HeavyLightDecomposition{
    static ArrayList<Integer>[] g, costs, edgeIdx;
    static int[] arr, chainIdx, chainStart, idxInArr;
    static int[] d, sub, edge;
    static int[][] lca;
    static int numChains;
    static SegmentTree st;
    static int n;

    public static void main(String[] args) throws Exception{
        // solution for QTree from SPOJ

        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
        
        int t = Integer.parseInt(r.readLine());
        for(int tc = 0; tc < t; tc++){
            r.readLine();
            n = Integer.parseInt(r.readLine());

            g = new ArrayList[n];
            costs = new ArrayList[n];
            edgeIdx = new ArrayList[n];

            for(int i = 0; i < n; i++){
                g[i] = new ArrayList<>();
                costs[i] = new ArrayList<>();
                edgeIdx[i] = new ArrayList<>();
            }

            for(int i = 0; i < n - 1; i++){
                int[] li = readArr(r);
                g[li[0] - 1].add(li[1] - 1);
                costs[li[0] - 1].add(li[2] - 1);
                edgeIdx[li[0] - 1].add(i);
                g[li[1] - 1].add(li[0] - 1);
                costs[li[1] - 1].add(li[2] - 1);
                edgeIdx[li[1] - 1].add(i);
            }

            preprocess();

            while(true){
                String l = r.readLine();
                if(l.equals("DONE"))
                    break;
                String[] li = l.split(" ");
                if(li[0].equals("QUERY")){
                    System.out.println(query(Integer.parseInt(li[1]) - 1, Integer.parseInt(li[2]) - 1));
                }else{
                    update(Integer.parseInt(li[1]) - 1, Integer.parseInt(li[2]));
                }
            }
        }
        
        r.close();
    }
    
    static void preprocess(){
        d = new int[n];
        lca = new int[31][n];
        sub = new int[n];
        edge = new int[n];

        dfs(0, -1);
        for(int i = 1; i < lca.length; i++){
            for(int j = 0; j < lca[0].length; j++){
                lca[i][j] = lca[i - 1][lca[i - 1][j]];
            }
        }

        numChains = 0;
        arr = new int[n];
        chainIdx = new int[n];
        chainStart = new int[n];
        Arrays.fill(chainStart, -1);
        idxInArr = new int[n];
        
        decompose(0, -1, -1, 0);
        st = new SegmentTree(n);
        st.construct(arr, 0, n - 1, 0);
    }

    static int query(int u, int v){
        int x = lca(u, v);
        return st.combineQuery(queryUp(u, x), queryUp(v, x));
    }

    static void update(int u, int val){
        st.update(0, n - 1, idxInArr[edge[u]], 0, val);
    }

    static int queryUp(int u, int v){
        if(u == v)
            return st.emptyQuery;
        int uChain;
        int vChain = chainIdx[v];
        int res = 0;
        
        while(true){
            uChain = chainIdx[u];

            if(uChain == vChain){
                if(u == v)
                    break;
                res = st.combineQuery(res, st.query(0, n - 1, idxInArr[u] + 1, idxInArr[v] + 1, 0));
            }

            res = st.combineQuery(res, st.query(0, n - 1, idxInArr[chainStart[uChain]], idxInArr[u] + 1, 0));

            u = chainStart[uChain];
            u = lca[0][u];
        }
        return res;
    }

    static void decompose(int u, int p, int cost, int arrIdx){
        if(chainStart[numChains] == -1){
            chainStart[numChains] = u;
        }
        chainIdx[u] = numChains;
        idxInArr[u] = arrIdx;
        arr[arrIdx] = cost;

        int heavyNode = -1;
        int heavyCost = -1;
        for(int i = 0; i < g[u].size(); i++){
            int v = g[u].get(i);
            int c = costs[u].get(i);
            if(v == p) continue;
            if(heavyNode == -1 || sub[heavyNode] < sub[v]){
                heavyNode = v;
                heavyCost = c;
            }
        }

        if(heavyNode != -1)
            decompose(heavyNode, u, heavyCost, arrIdx + 1);
        
        for(int i = 0; i < g[u].size(); i++){
            int v = g[u].get(i);
            int c = costs[u].get(i);
            if(v == p || v == heavyNode) continue;
            numChains++;
            decompose(v, u, c, arrIdx + 1);
        }
    }

    static void dfs(int u, int p){
        if(p >= 0){
            lca[0][u] = p;
            d[u] = d[p] + 1;
        }
        sub[u] = 1;
        for(int i = 0; i < g[u].size(); i++){
            int v = g[u].get(i);
            if(v == p) continue;
            edge[edgeIdx[u].get(i)] = v;
            dfs(v, u);
            sub[u] += sub[v];
        }
    }

    static int lca(int u, int v){
        if(d[u] > d[v]){
            int t = u;
            u = v;
            v = t;
        }
        int depth = d[v] - d[u];
        for(int i = 0; i < lca.length; i++){
            if((depth & (1 << i)) != 0)
                v = lca[i][v];
        }
        if(u == v)
            return u;
        for(int i = lca.length - 1; i >= 0; i--){
            if(lca[i][u] != lca[i][v]){
                u = lca[i][u];
                v = lca[i][v];
            }
        }
        return lca[0][u];
    }

    static class SegmentTree{
        int n;
        int[] seg;
        
        SegmentTree(int n){
            this.n = n;
            this.seg = new int[n * 4];
        }
        
        int emptyQuery = 0;
        
        int combineQuery(int a, int b){
            return Math.max(a, b);
        }
        
        int combineUpdate(int o, int val){
            return val;
        }
        
        int construct(int[] arr, int l, int r, int i){
            if(l == r){
                seg[i] = arr[l];
                return seg[i];
            }
            int m = (l + r) >>> 1;
            seg[i] = combineQuery(construct(arr, l, m, i * 2 + 1), construct(arr, m + 1, r, i * 2 + 2));
            return seg[i];
        }
        
        int construct(int l, int r, int i, int val){
            if(l == r){
                seg[i] = val;
                return seg[i];
            }
            int m = (l + r) >>> 1;
            seg[i] = combineQuery(construct(l, m, i * 2 + 1, val), construct(m + 1, r, i * 2 + 2, val));
            return seg[i];
        }
        
        int query(int l, int r, int ql, int qr, int i){
            if(l >= ql && qr >= r){
                return seg[i];
            }
            if(r < ql || l > qr){
                return emptyQuery;
            }
            int m = (l + r) >>> 1;
            return combineQuery(query(l, m, ql, qr, i * 2 + 1), query(m + 1, r, ql, qr, i * 2 + 2));
        }
        
        void update(int l, int r, int ui, int i, int val){
            if(r < ui || l > ui){
                return;
            }
            if(l == r){
                seg[i] = combineUpdate(seg[i], val);
                return;
            }
            int m = (l + r) >>> 1;
            update(l, m, ui, i * 2 + 1, val);
            update(m + 1, r, ui, i * 2 + 2, val);
            seg[i] = combineQuery(seg[i * 2 + 1], seg[i * 2 + 2]);
        }
    }

    static int[] readArr(BufferedReader r) throws Exception{
        String[] l = r.readLine().split(" ");
        int[] a = new int[l.length];
        for(int i = 0; i < l.length; i++)
            a[i] = Integer.parseInt(l[i]);
        return a;
    }
}