
public class ConvexHullTrick{
	public static void main(String[] args){
		ConvexHullTrick c = new ConvexHullTrick(3);
		c.add(2.0 / 3.0, 0);
		c.add(0, 4);
		c.add(-1.0 / 2.0, 1);
		c.add(-3, 5);
		System.out.println(c.query(-5)[0] + " " + c.query(-5)[1]);
		System.out.println(c.idx);
	}
	
	Segment[] q;
	int idx = 0;
	
	ConvexHullTrick(int maxSize){
		q = new Segment[maxSize];
	}
	
	//lines need to be in decending order of slope
	void add(double m, double b){
		Line l = new Line(m, b);
		while(idx - 2 >= 0 && (q[idx - 1].l.equals(l) || q[idx - 2].l.intersect(l)[0] < q[idx - 2].l.intersect(q[idx - 1].l)[0])){
			idx--;
		}
		
		if(idx == 0){
			q[idx] = new Segment(l, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
		}else{
			q[idx] = new Segment(l, l.intersect(q[idx - 1].l)[0], Double.POSITIVE_INFINITY);
			q[idx - 1].e = l.intersect(q[idx - 1].l)[0];
		}
		
		idx++;
	}
	
	double[] query(double x){
		int l = 0, r = idx - 1, res = -1;
		while(l <= r){
			int m = l + (r - l) / 2;
			if(x <= q[m].s){
				r = m - 1;
			}else if(x >= q[m].e){
				l = m + 1;
			}else{
				res = m;
				break;
			}
		}
		
		if(res != -1){
			return new double[]{x, q[res].l.y(x)};
		}else{
			return null;
		}
	}
	
	class Segment{
		Line l;
		double s, e;
		
		Segment(Line l, double s, double e){
			this.l = l;
			this.s = s;
			this.e = e;
		}
	}
	
	class Line{
		double m, b;
		
		Line(double m, double b){
			this.m = m;
			this.b = b;
		}
		
		double y(double x){
			return m * x + b;
		}
		
		double[] intersect(Line o){
			if(parallel(o)){
				return null;
			}
			if(m == Double.POSITIVE_INFINITY){
				double x = b;
				double y = o.y(x);
				return new double[]{x, y};
			}else if(o.m == Double.NEGATIVE_INFINITY){
				double x = o.b;
				double y = y(x);
				return new double[]{x, y};
			}else{
				double x = (o.b - b) / (m - o.m);
				double y = y(x);
				return new double[]{x, y};
			}
		}
		
		boolean parallel(Line o){
			return Math.abs(m - o.m) < 1e-10;
		}
		
		@Override
		public int hashCode(){
			final int prime = 31;
			int result = 1;
			long temp;
			temp = Double.doubleToLongBits(b);
			result = prime * result + (int)(temp ^ (temp >>> 32));
			temp = Double.doubleToLongBits(m);
			result = prime * result + (int)(temp ^ (temp >>> 32));
			return result;
		}
		
		@Override
		public boolean equals(Object obj){
			if(this == obj)
				return true;
			if(obj == null)
				return false;
			if(getClass() != obj.getClass())
				return false;
			Line other = (Line)obj;
			if(Double.doubleToLongBits(b) != Double.doubleToLongBits(other.b))
				return false;
			if(Double.doubleToLongBits(m) != Double.doubleToLongBits(other.m))
				return false;
			return true;
		}
	}
}
