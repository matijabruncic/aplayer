package org.mats990.song;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.Executors;
import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
@Slf4j
public class SongService {

    @Autowired
    private SongUrlRepository songUrlRepository;
    private Song song;

    public void play(String songName) {
        log.info("Playing: {}", songName);
        List<String> links = songUrlRepository.getLinks(songName);
        String link = links.iterator().next();
        Song song = new Song(link);
        song.play();
        this.song = song;
    }

    private void redirectInputStream(InputStream inputStream, Consumer<String> lineConsumer) {
        Executors.newSingleThreadExecutor().execute(()->{
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            try {
                while ((line = bufferedReader.readLine()) != null) {
                    lineConsumer.accept(line);
                }
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }
        });
    }

    public void stop() {
        this.song.stop();
        this.song = null;
    }

    private class Song {
        private final String link;
        private String fileName;
        private Thread downloadThread;
        private Thread playThread;

        public Song(String link) {
            this.link = link;
        }

        public void play() {
            Thread downloadThread = new Thread(() -> {
                Process ytdl= null;
                try {
                    log.info(link);
                    String id = link.replace("https://www.youtube.com/watch?v=", "");
                    ytdl = new ProcessBuilder("ytdl", "-a", id)
                            .start();
                    redirectInputStream(ytdl.getInputStream(), (line) -> {
                        Pattern compile = Pattern.compile("-Downloading '(.*)' \\[.*");
                        Matcher matcher = compile.matcher(line);
                        if (line.trim().isEmpty()) {
                            return;
                        } else if (line.contains("Rate:")) {
                            return;
                        } else if (matcher.matches()) {
                            fileName = matcher.group(1);
                        }
                        log.info(line);
                    });
                    redirectInputStream(ytdl.getErrorStream(), log::error);
                    ytdl.waitFor();
                    if (ytdl.exitValue() != 0) {
                        log.error("Error");
                    }
                } catch (InterruptedException ie){
                    ytdl.destroyForcibly();
                    Thread.currentThread().interrupt();
                    return;
                } catch (Exception e) {
                    log.error(e.getMessage(), e);
                }
            });

            Thread playThread = new Thread(() -> {
                log.info("playing song ...{}", link);
                while (fileName == null) {
                    try {
                        Thread.sleep(200);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                Process cvlc = null;
                try {
                    if (!new File(fileName).exists()) {
                        fileName = fileName.concat(".temp");
                    }
                    cvlc = new ProcessBuilder("cvlc", fileName)
                            .start();
                    redirectInputStream(cvlc.getInputStream(), log::info);
                    redirectInputStream(cvlc.getErrorStream(), (line)->{
                        if (line.endsWith("using the dummy interface module..."))
                            return;
                        log.error(line);
                    });
                    cvlc.waitFor();
                    if (cvlc.exitValue() != 0) {
                        log.error("Error");
                    }
                } catch (InterruptedException ie){
                    cvlc.destroyForcibly();
                    Thread.currentThread().interrupt();
                    return;
                } catch (Exception e) {
                    log.error(e.getMessage(), e);
                    return;
                }
            });
            downloadThread.start();
            playThread.start();

            this.downloadThread = downloadThread;
            this.playThread = playThread;
        }

        public void stop() {
            while (downloadThread.isAlive() || playThread.isAlive()) {
                downloadThread.interrupt();
                playThread.interrupt();
            }

        }
    }
}
