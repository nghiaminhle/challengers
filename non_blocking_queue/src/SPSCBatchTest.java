
/**
 * Batch Testing
 */

public class SPSCBatchTest {
	
	private final static int BATCH_SIZE = 1024;
	
	public static void main(String[] args) throws Exception {
		
		System.out.println("SP-SC Test");
		
		testQueue();
		
		System.out.println("-End!-");
	}

	private static void testQueue() throws Exception {
		
		RingBufferSPSC<Integer[]> q = new RingBufferSPSC<Integer[]>();

		int rounds = 20;
		long pace = 0;
		long min = 0;
		long max = 0;
		int noThreads = 1;
		int noItems = 1000000;
		for (int r = 0; r < rounds; r++) {
			System.out.println(r);

			long result = test(noThreads, noItems, q);
			pace += result;
			if (result > max) {
				max = result;
				if (min == 0) {
					min = max;
				}
			}
			if (result < min) {
				min = result;
			}
		}
		System.out.println("Average throughput: " + (pace / rounds) + " items/s. Max: " + max + " items/s. Min: " + min
				+ " items/s");
	}

	private static long test(int noThreads, int noItems, RingBufferSPSC<Integer[]>queue) {
		SPSCConsumerThread[] consumers = new SPSCConsumerThread[noThreads];
		
		for(int i=0; i<consumers.length; i++) {
			consumers[i] = new SPSCConsumerThread(queue);
			consumers[i].start();
		}
		
		long start = System.currentTimeMillis();
		
		for(int i=0; i<noItems; i++) {
			Integer[] batch = new Integer[BATCH_SIZE];
			for(int j=0; j<batch.length; j++) {
				batch[j] = i;
			}
			while (!queue.enqueue(batch)) {}
		}
		
		while(!queue.isEmpty()) {
			//Thread.onSpinWait();
		}
		
		long elapsed = (System.currentTimeMillis() - start);
		long pace = (long)noItems * 1000 * BATCH_SIZE / elapsed;
		
		System.out.println(noItems + " works @ " + elapsed + "ms. Pace: " + pace + " items/s");
		
		start = System.nanoTime();
		
		for(int i=0; i<consumers.length; i++) {
			consumers[i].cancel();
		}

		for(int i=0; i<consumers.length; i++) {
			try {
				consumers[i].join();
			} catch (InterruptedException e) {
			}
			long expected = (long)noItems * (noItems - 1) * BATCH_SIZE / 2;
			if (consumers[i].getCounter() != expected) {
				throw new RuntimeException("Consumers dequeue mismatch, expected: " + expected + ", actual: " + consumers[i].getCounter());
			}
		}
		return pace;
	}
}

class SPSCConsumerThread extends Thread {
	
	private RingBufferSPSC<Integer[]> queue;
	
	private long counter = 0;

	public SPSCConsumerThread(RingBufferSPSC<Integer[]> queue) {
		this.queue = queue;
	}
	
	@Override
	public void run() {
		while(!Thread.currentThread().isInterrupted()) {
			while(!Thread.currentThread().isInterrupted() && queue.isEmpty()) {
				//Thread.onSpinWait();
			}
			Integer[] item = queue.dequeue();
			if (item != null) {
				for(int i=0; i<item.length; i++) {
					counter += item[i];
				}
			}
		}
	}
	
	public void cancel() {
		interrupt();
	}
	
	public long getCounter() {
		return counter;
	}
}