/** ShinyStatClient
 * ShinyStatClient is an adorable little java class whose sole purpose is to
 * contact a ShinyMUD game server and then report certain game statistics.
 *
 * For simple text example, invoke the main() with the following arguments:
 *      incendiarysoftware.com 4111
 *
 * @author Jess Coulter
 */


import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ShinyStatClient {
    
    /** The game server's hostname */
    private String host;
    /** The game server's port */
    private int port;
    /** The game server's raw response data */
    private String rawResult;
    /** Will be the string "Online" or "Offline" */
    private String gameStatus;
    /** a human readible date of when the server was restarted */
    private String uptime;
    /** the names of players currently logged in (will be null if the server
        is offline) */
    private String[] playerNames;
    
    /**
        ShinyStatClient creates a shinyStatClient object, which contacts a
        ShinyMUD game server to gather game Statistics. Its methods then 
        generate cute reports based on that data.
        
        @throws ShinyStatException If something goes terribly awry (such as
        the given hostname not existing) and ShinyStatClient can't continue,
        a ShinyStatException will be thrown.
    */
    public ShinyStatClient(String shinyHost, int shinyPort) throws ShinyStatException {
        setPort(shinyPort);
        setHost(shinyHost);
        contactServer();
    }
    
    /**
        main provides a simple example of ShinyStatClient in action. It takes
        a hostname and port as args (in that order), and prints a pretty text
        report.
    */
    public static void main(String[] args) {
        
        // Make sure we have two arguments
        if (args.length != 2) { 
            System.out.println("Usage: java ShinyStatClient hostname port");
        }
        
        // Don't let the user pass an argument for port that's not an int
        int shinyPort = 0;
        try {
            shinyPort = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("ERROR: The port must be a number.");
        }
        
        try{
            ShinyStatClient shiny = new ShinyStatClient(args[0], shinyPort);
            System.out.println(shiny.reportPrettyText());
        } catch (ShinyStatException e) {
            System.out.println(e.getMessage());
        }
    }
    
    /**
        contactServer takes it upon itself to get (and parse) data from the 
        ShinyMUD game server by the host and port given to the constructor.
        
        @throws ShinyStatException If something goes terribly awry (such as
        the given hostname not existing) and ShinyStatClient can't continue,
        a ShinyStatException will be thrown.
    */
    public void contactServer() throws ShinyStatException {
        // Do server contact
        try {
            Socket shinySocket = new Socket(host, port);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                                                       shinySocket.getInputStream()));
            // rawResult is going to look like the following:
            // uptime:name1,name2
            rawResult = in.readLine();
        } catch (UnknownHostException e){
            throw new ShinyStatException("ERROR: Unknown host \"" + host + "\"");
        } catch (IOException e) {
            // in this case, I believe we can assume the game is offline
            gameStatus = "offline";
        } catch (SecurityException e) {
            // Not really sure what went wrong here, but let's throw an error
            // since we won't be able to continue
            throw new ShinyStatException(e.getMessage());
        }
        
        if (gameStatus != "offline") {
            // If we've gotten this far and the game isn't online, that means
            // everything (probably) went fine, and we can assume the game is
            // online
            gameStatus = "online";
        
            // Now that we've finished contacting the server, let's parse the
            // data it gave us
        
            String[] temp = rawResult.split(":");
        
            // Warning: sillyness ensues:
            // The date we're getting back from the ShinyStatServer is going to be
            // a string version of a double. It also represents the time in seconds,
            // not milliseconds, so we're going to have to multiply our double by
            // 1000 to get the correct number before we finally cast it to a long. 
            // Harsh.
            Date date = new Date((long) (Double.parseDouble(temp[0]) * 1000));
        
            // But now that that's sorted, we can get a lovely human readible version
            uptime = new SimpleDateFormat("MMM d, yyyy").format(date);
        
            if (temp.length > 1) {
                // Excellent, that means there are players online! We should parse
                // their names into an array
                playerNames = temp[1].split(",");
            }
        }
    }
    
    // ***************** Attribute Getters and Setters ***************** //
    public void setHost(String shinyHost) {
        host = shinyHost;
    }
    
    public void setPort(int shinyPort) {
        port = shinyPort;
    }
    
    public String getHost() {
        return host;
    }
    
    public int getPort() {
        return port;
    }
    
    // ***************** ReportMethods ***************** //
    
    /**
        reportHTML would be really useful if it were written. It would return
        a report formatted in HTML for display on a webpage. So Neat!
        
        @param cssContext a string containing a class name for which all 
        html elements would decend. This makes it easy to style only what
        gets returned by this report
    */
    
    public String reportHTML(String cssContext) {
        // return some nice HTML. Not foo, don't return foo.
        return "foo";
    }
    
    /**
        reportRawString just returns the string it got from the ShinyMUD server.
        No more, no less.
    */
    public String reportRawString() {
        return rawResult;
    }
    
    /**
        reportPrettyText gives us a nice, clean, text-based report of game
        statistics. It'll look something like the following:
            Checking server at host: incendiarysoftware.com, port: 4112
            Game server is: ONLINE
            The server was last restarted on: Aug 30, 2010
            There is 1 player online right now:
              surrey
    */
    public String reportPrettyText() {
        // Return a nice text version
        String result = String.format("Checking server at host: %s, port: %d\n" +
                                      "Game server is: %s\n",
                                      host, port, gameStatus.toUpperCase());
        
        if (gameStatus == "online") {
            // If the game is online, let's add the staticstics
            String playerStr = "";
            if (playerNames == null) {
                playerStr = "There are no players online right now.";
            } else if (playerNames.length == 1) {
                playerStr = String.format("There is 1 player online right now:\n  %s",
                                          playerNames[0]);
            } else {
                playerStr = String.format("There are %d players online right now:", 
                                          playerNames.length);
                for (String name: playerNames) {
                    playerStr += "\n  " + name;
                }
            }
            
            result += String.format("The server was last restarted on: %s\n%s\n",
                                    uptime, playerStr);
        } else {
            // The game is offline.
            result += "Down for maintenance. Back up soon!";
        }
        
        return result;
    }
}

class ShinyStatException extends Exception {
    String err;
    
    public ShinyStatException() {
        super();
        err = "There was an error in the ShinyStatClient.";
    }
    
    public ShinyStatException(String errorMsg) {
        super(errorMsg);
        err = errorMsg;
    }
    
    public String getError() {
        return err;
    }
}