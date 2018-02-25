package org.mats990.cron;

import lombok.extern.slf4j.Slf4j;
import org.mats990.song.SongNameService;
import org.mats990.song.SongService;
import org.mats990.wireless.DeviceStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class StatusChecker {

    @Autowired
    private DeviceStatusService deviceStatusService;
    @Autowired
    private SongNameService songNameService;
    @Autowired
    private SongService songService;

    private boolean wasConnected = false;

    @Scheduled(fixedRate = 1_000L)
    public void run() {
        boolean connected = deviceStatusService.isConnected();
        boolean changed = wasConnected != connected;
        if (changed && !wasConnected) {
            String songName = songNameService.randomSongName();
            log.info("You've just got home and I got a song for you: {}", songName);
            songService.play(songName);
        } else if (changed) {
            songService.stop();
            log.info("Stopped playing music");
        }
        wasConnected = connected;
    }
}
