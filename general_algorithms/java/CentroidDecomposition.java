import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.HashSet;

public class CentroidDecomposition{
    static HashSet<Integer>[] g;
    static int[] d;
    static int[][] lca;
    static int[] sub;
    static int nodes;
    static int[] parent;
    static int[] res;

    public static void main(String[] args) throws Exception{
        // solution to Xenia and Tree from Codeforces
        
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
        
        int[] l1 = readArr(r);
        int n = l1[0];
        int m = l1[1];
        g = new HashSet[n];
        for(int i = 0; i < n; i++) g[i] = new HashSet<>();
        for(int i = 0; i < n - 1; i++){
            int[] li = readArr(r);
            g[li[0] - 1].add(li[1] - 1);
            g[li[1] - 1].add(li[0] - 1);
        }
        
        preprocess(n);

        update(0);
        for(int i = 0; i < m; i++){
            int[] li = readArr(r);
            if(li[0] == 1){
                update(li[1] - 1);
            }else{
                System.out.println(query(li[1] - 1));
            }
        }

        r.close();
    }
    
    static void preprocess(int n){
        d = new int[n];
        lca = new int[31][n];

        dfs(0, -1);
        for(int i = 1; i < lca.length; i++){
            for(int j = 0; j < lca[0].length; j++){
                lca[i][j] = lca[i - 1][lca[i - 1][j]];
            }
        }
        
        sub = new int[n];
        parent = new int[n];
        res = new int[n];
        Arrays.fill(res, Integer.MAX_VALUE);

        decompose(0, -1);
    }

    static void dfs(int u, int p){
        if(p >= 0){
            lca[0][u] = p;
            d[u] = d[p] + 1;
        }
        for(int v : g[u]){
            if(v == p) continue;
            dfs(v, u);
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

    static int dist(int u, int v){
        return d[u] + d[v] - d[lca(u, v)] * 2;
    }

    static void dfs2(int u, int p){
        nodes++;
        sub[u] = 1;
        for(int v : g[u]){
            if(v == p) continue;
            dfs2(v, u);
            sub[u] += sub[v];
        }
    }

    static int centroid(int u, int p){
        for(int v : g[u]){
            if(v == p || sub[v] <= nodes / 2) continue;
            return centroid(v, u);
        }
        return u;
    }

    static void decompose(int u, int p){
        nodes = 0;
        dfs2(u, -1);
        int centroid = centroid(u, -1);
        if(p == -1)
            p = centroid;
        parent[centroid] = p;
        for(int v : g[centroid]){
            g[v].remove(centroid);
            decompose(v, centroid);
        }
        g[centroid].clear();
    }

    static void update(int u){
        int centroid = u;
        while(true){
            res[centroid] = Math.min(res[centroid], dist(centroid, u));
            if(centroid == parent[centroid])
                break;
            centroid = parent[centroid];
        }
    }

    static int query(int u){
        int centroid = u;
        int ans = Integer.MAX_VALUE;
        while(true){
            if(res[centroid] != Integer.MAX_VALUE)
                ans = Math.min(ans, dist(u, centroid) + res[centroid]);
            if(centroid == parent[centroid])
                break;
            centroid = parent[centroid];
        }
        return ans;
    }

    static int[] readArr(BufferedReader r) throws Exception{
        String[] l = r.readLine().split(" ");
        int[] a = new int[l.length];
        for(int i = 0; i < l.length; i++)
            a[i] = Integer.parseInt(l[i]);
        return a;
    }
}