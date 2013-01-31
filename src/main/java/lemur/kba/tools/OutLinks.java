/*******************************************************************************
 * Copyright 2012 Edgar Meij
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/
package lemur.kba.tools;

import java.io.FileInputStream;
import java.util.List;
import java.util.zip.GZIPInputStream;

import kba.StreamItem;

import net.htmlparser.jericho.Element;
import net.htmlparser.jericho.HTMLElementName;
import net.htmlparser.jericho.Source;

import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TIOStreamTransport;

public class OutLinks {

    /**
     * Extract the links included in the body field of the records from the KBA stream.
     * 
     * @param args
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {

        if (args.length == 0) {
            System.err.println("Usage: OutLinks foo.thrift.gz");
            System.exit(1);
        }

        FileInputStream fis = new FileInputStream(args[0]);
        GZIPInputStream gis = new GZIPInputStream(fis);
        TProtocol tp = new TBinaryProtocol.Factory().getProtocol(new TIOStreamTransport(gis));
        StreamItem si = new StreamItem();

        int nRecords = 0;
        int nErrors = 0;

        while (fis.available() > 0) {
            try {

                si.read(tp);

                try {
                    String body = new String(si.body.raw.array(), si.body.encoding);
                    Source source = new Source(body);

                    List<Element> links = source.getAllElements(HTMLElementName.A);
                    for (Element a : links) {
                        String href = a.getAttributeValue("href");
                        if (href != null)
                            System.out.println(href);
                    }
                    nRecords += 1;

                } catch (Exception e) {
                    nErrors += 1;
                }

            } catch (Exception e) {
                e.printStackTrace();
                break;
            }
        }

        System.err.printf("Records: %s Errors: %s\n", nRecords, nErrors);

    }
}
