package org.mats990.song;

import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.apache.commons.io.FileUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Attribute;
import org.jsoup.nodes.Attributes;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Collection;
import java.util.List;

@Component
@Slf4j
public class SongUrlRepository {
    private final File folder = new File("/var/lib/aplayer/videolinks/");
    private final File config = new File("/etc/aplayer/songs");


    @Scheduled(fixedRate = 1000*60*60)
    public void run(){
        try {
            CSVParser parse = CSVParser.parse(config, Charset.defaultCharset(), CSVFormat.DEFAULT);
            for (CSVRecord line : parse){
                String artist = line.get(1);
                String songName = line.get(2);
                fetchLinks(artist + " " + songName);
                log.info("Updated links for: {} - {}", artist, songName);
            }
        } catch (IOException e) {
            log.error(e.getMessage(), e);
        }
    }

    private void fetchLinks(String songName) {
        try {
            String encodedSongName = URLEncoder.encode(songName, "UTF-8");
            String response = Unirest.get("https://www.youtube.com/results?search_query="+encodedSongName).asString().getBody();
            Document document = Jsoup.parse(response);
            Elements li = document.select("#results")
                    .select("ol").first()
                    .select("li");
            li.next();
            Elements elements = li.next()
                    .select("ol")
                    .select("li")
                    .select("a[aria-hidden=\"true\"]");
            Collection<String> links = new ArrayList<>();
            for (Element element : elements) {
                Attributes attributes = element.attributes();
                for (Attribute attribute : attributes) {
                    if ("href".equals(attribute.getKey())){
                        String link = "https://www.youtube.com" + attribute.getValue();
                        links.add(link);
                    }
                }
            }
            File songFile = new File(folder, encode(songName));
            FileUtils.writeLines(songFile, links);
        } catch (UnirestException | NoSuchAlgorithmException | IOException e) {
            log.error(e.getMessage(), e);
        }
    }

    private String encode(String songName) throws NoSuchAlgorithmException {
        MessageDigest messageDigest = MessageDigest.getInstance("SHA-256");
        messageDigest.update(songName.getBytes());
        return new String(Base64.getUrlEncoder().encode(messageDigest.digest()));
    }

    public List<String> getLinks(String songName) {
        try {
            String songNameEncoded = encode(songName);
            List<String> strings = FileUtils.readLines(new File(folder, songNameEncoded), Charset.defaultCharset());
            return strings;
        } catch (IOException | NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }
}
