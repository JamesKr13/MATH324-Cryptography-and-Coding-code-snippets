package assignment1;

import assignment1.cli.ArgumentBundle;
import assignment1.crypto.CipherUtils;
import assignment1.crypto.Encryptor;
import org.junit.jupiter.api.Test;

import javax.crypto.SecretKey;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Random;


public class CryptoBenchMarkTests {

    private Path csvFile;
    private static final int[] KEY_SIZES = {128, 192, 256};
    private static final String[] MODES = {"ECB", "CBC", "CTR", "GCM"};

    @Test
    public void runAllBenchmarks() throws IOException {
        this.BenchmarkCSV("benchmark.csv");
        for (String mode : MODES) {
            for (int keySize : KEY_SIZES) {
                this.runBenchmark(mode, keySize);
            }
        }

    }

    public void BenchmarkCSV(String fileName) throws IOException {
        csvFile = Path.of(fileName);

        // If file exists, delete it to start fresh
        if (Files.exists(csvFile)) {
            Files.delete(csvFile);
        }

        // Create file and write header
        try (FileWriter fw = new FileWriter(csvFile.toFile())) {
            fw.write("mode,keySize,input size, time (ms)\n");
        }
    }



    /**
     * Generate a random byte array of given size.
     */
    private static byte[] generateInput(long size) {
        int arraySize = (int) Math.min(size, Integer.MAX_VALUE);
        byte[] data = new byte[arraySize];
        new Random().nextBytes(data);
        return data;
    }

    public static void writeCsvRow(Path csvFile, String mode, String keySize, String time, long size) throws IOException {
        try (FileWriter fw = new FileWriter(csvFile.toFile(), true)) {
            fw.write(String.format("%s,%s,%s, %s\n", mode, keySize, size, time));
        }
    }

    /**
     * Run benchmark for a given AES mode and key size.
     * @param mode AES mode (e.g., "CBC", "GCM")
     * @param keySize AES key size (128, 192, 256)
     * @throws IOException
     */
    public void runBenchmark(String mode, int keySize) throws IOException {
        // Generate IV once
        byte[] iv = new byte[16];
        new Random().nextBytes(iv);

        // Input sizes from 1B to 100MB (roughly ×10 scaling)
        long[] sizes = {1, 10, 100, 1024, 10 * 1024, 100 * 1024, 1024 * 1024, 10 * 1024 * 1024, 100 * 1024 * 1024};

        for (long size : sizes) {
            byte[] input = generateInput(size);

            // Generate random AES key
            SecretKey key = CipherUtils.generateRandomAESKey(keySize);
            // Prepare arguments for in-memory encryption
            ArgumentBundle args = new ArgumentBundle();
            args.encrypt = true;                       // we are encrypting
            args.input = input;               // path to generated input
            args.outFile = null;                        // output to memory or temp file
            args.keyByte = CipherUtils.generateRandomKey(16);      // AES-128 key (16 bytes)
            args.iv = CipherUtils.generateRandomIV(16);            // 16-byte IV for CBC/CFB, null for ECB
            args.mode = mode;                          // AES mode
            args.cipherSize = 128;                      // in bits
            args.password = null;                        // not used here
            // Measure only encryption computation
            long durationMs;
            try {
                int repeats = size < 16 ? 1000 : 1;
                long totalTimeNs = 0;
                for (int i = 0; i < repeats; i++) {
                    long start = System.nanoTime();
                    Encryptor.encrypt(args);
                    long end = System.nanoTime();
                    totalTimeNs += (end - start);
                }
                long durationNs = totalTimeNs / repeats;
                durationMs = durationNs / 1_000;

            } catch (Exception e) {
                throw new RuntimeException(e);
            }



            // Write results to CSV
            writeCsvRow(this.csvFile, mode, String.valueOf(keySize), String.valueOf(durationMs), size);
            
        }

    }


}
