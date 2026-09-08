import re

def update_compiler_service():
    with open('src/main/java/com/cs/bugdetector/service/CompilerService.java', 'r', encoding='utf-8') as f:
        content = f.read()

    new_method = """
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
                        output.append(line).append("\\n");
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
    """

    if "executeMultipleCommands" not in content:
        content = content.replace("private void deleteDirectoryRecursively", new_method + "\n    private void deleteDirectoryRecursively")

    with open('src/main/java/com/cs/bugdetector/service/CompilerService.java', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CompilerService")

if __name__ == "__main__":
    update_compiler_service()
