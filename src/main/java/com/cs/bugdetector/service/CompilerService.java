package com.cs.bugdetector.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

@Service
@Slf4j
public class CompilerService {

    private static final long TIMEOUT_SECONDS = 10;
    private static final String TEMP_DIR_PREFIX = "devsentry_analysis_";

    public CompilerResult executeWithTimeout(String[] command, String sourceCode, String filename) {
        Path tempDir = null;
        try {
            // 1. Create temporary directory
            tempDir = Files.createTempDirectory(TEMP_DIR_PREFIX + UUID.randomUUID().toString());
            File workingDir = tempDir.toFile();

            // 2. Write source code to file
            Path sourceFile = tempDir.resolve(filename);
            Files.writeString(sourceFile, sourceCode);

            // 3. Setup process builder
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.directory(workingDir);
            pb.redirectErrorStream(true); // Combine stdout and stderr

            // 4. Start process
            Process process = pb.start();

            // 5. Read output
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                    if (output.length() > 50000) { // Safety limit for output size
                        output.append("... [Output truncated due to size limit]");
                        break;
                    }
                }
            }

            // 6. Wait for completion with timeout
            boolean completed = process.waitFor(TIMEOUT_SECONDS, TimeUnit.SECONDS);

            if (!completed) {
                process.destroyForcibly();
                log.warn("Process timed out: {}", String.join(" ", command));
                return new CompilerResult(false, -1, "TIMEOUT: Process took too long to execute.", true);
            }

            int exitCode = process.exitValue();
            return new CompilerResult(exitCode == 0, exitCode, output.toString(), false);

        } catch (Exception e) {
            log.error("Error executing compiler command", e);
            return new CompilerResult(false, -1, "Execution Error: " + e.getMessage(), false);
        } finally {
            // 7. Cleanup temp directory safely
            if (tempDir != null) {
                try {
                    deleteDirectoryRecursively(tempDir);
                } catch (IOException e) {
                    log.warn("Failed to delete temp directory: {}", tempDir, e);
                }
            }
        }
    }

    
    public CompilerResult executeMultipleCommands(String[][] commands, String sourceCode, String filename) {
        Path tempDir = null;
        try {
            tempDir = Files.createTempDirectory(TEMP_DIR_PREFIX + UUID.randomUUID().toString());
            File workingDir = tempDir.toFile();

            Path sourceFile = tempDir.resolve(filename);
            Files.writeString(sourceFile, sourceCode);

            StringBuilder finalOutput = new StringBuilder();
            boolean success = true;
            int lastExitCode = 0;

            for (String[] command : commands) {
                ProcessBuilder pb = new ProcessBuilder(command);
                pb.directory(workingDir);
                pb.redirectErrorStream(true);

                Process process = pb.start();

                StringBuilder output = new StringBuilder();
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        output.append(line).append("\n");
                        if (output.length() > 50000) {
                            output.append("... [Output truncated due to size limit]");
                            break;
                        }
                    }
                }

                boolean completed = process.waitFor(TIMEOUT_SECONDS, TimeUnit.SECONDS);

                if (!completed) {
                    process.destroyForcibly();
                    log.warn("Process timed out: {}", String.join(" ", command));
                    return new CompilerResult(false, -1, "TIMEOUT: Process took too long to execute.", true);
                }

                lastExitCode = process.exitValue();
                finalOutput.append(output.toString());
                
                if (lastExitCode != 0) {
                    success = false;
                    break;
                }
            }

            return new CompilerResult(success, lastExitCode, finalOutput.toString(), false);

        } catch (Exception e) {
            log.error("Error executing compiler command", e);
            return new CompilerResult(false, -1, "Execution Error: " + e.getMessage(), false);
        } finally {
            if (tempDir != null) {
                try {
                    deleteDirectoryRecursively(tempDir);
                } catch (IOException e) {
                    log.warn("Failed to delete temp directory: {}", tempDir, e);
                }
            }
        }
    }
    
    private void deleteDirectoryRecursively(Path path) throws IOException {
        if (Files.exists(path)) {
            try (Stream<Path> walk = Files.walk(path)) {
                walk.sorted(Comparator.reverseOrder())
                    .map(Path::toFile)
                    .forEach(File::delete);
            }
        }
    }

    public record CompilerResult(boolean success, int exitCode, String output, boolean isTimeout) {}
}
