package org.mats990.song;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;
import java.util.Random;

@Component
@Slf4j
public class SongNameService {
    Random random = new Random();
    private final File config = new File("/etc/aplayer/songs");

    public String randomSongName() {

        CSVParser parse;
        try {
            parse = CSVParser.parse(config, Charset.forName("UTF-8"), CSVFormat.DEFAULT);
            List<CSVRecord> records = parse.getRecords();
            int i = random.nextInt(records.size());
            return records.get(i).get(1) + " " + records.get(i).get(2);
        } catch (IOException e) {
            log.error(e.getMessage(), e);
            throw new IllegalStateException(e);
        }
    }
}
