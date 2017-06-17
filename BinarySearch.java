package reference;

public class BinarySearch {
	public static void main(String[] args){
		System.out.println(binarySearch(new int[]{1, 1, 1, 2, 2, 2, 2, 3}, 3, false));
	}
	
	private static int binarySearch(int[] arr, int val, boolean leftMost){
		int left = 0, right = arr.length - 1, result = -1;
		
		while(left <= right){
			int mid = left + (right - left) / 2;
			
			if(arr[mid] == val){
				result = mid;
				if(leftMost){
					right = mid - 1;
				}else{
					left = mid + 1;
				}
			}else if(arr[mid] > val){
				right = mid - 1;
			}else{
				left = mid + 1;
			}
		}
		
		return result;
	}
}
