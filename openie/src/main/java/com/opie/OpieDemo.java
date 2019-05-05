package com.opie;
import java.util.Arrays;

import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.simple.*;

public class OpieDemo {

	public static void main(String[] args) throws Exception {
	    // Create a CoreNLP document
	   // Document doc = new Document("Obama was born in Hawaii. He is our president.");
		
		Document doc = new Document("V1 was northbound on a five lane, not physically divided, dry roadway, preparing to turn left at the intersection. V2 was southbound on a five lane, not physically divided, dry roadway. V1 proceeded to turn left when impact occurred. The front of V2 contacted the right side of V1. Upon impact, V1 rotated counter-clockwise, coming to final rest facing west in the southbound lane of travel. Both passengers of V2 were transported to the hospital for minor injuries and both vehicles had been towed from the scene.");
		
	    // Iterate over the sentences in the document
	    for (Sentence sent : doc.sentences()) {
	      // Iterate over the triples in the sentence
	      for (RelationTriple triple : sent.openieTriples()) {
	    	  
	    	 //System.out.println(triple.toString());
	    	 String[] split = triple.toString().split("\t");
	    	 System.out.println(Arrays.toString(split));
	        // Print the triple
	       /* System.out.println(triple.confidence + "\t" +
	            triple.subjectLemmaGloss() + "\t" +
	            triple.relationLemmaGloss() + "\t" +
	            triple.objectLemmaGloss());*/
	      }
	    }
	  }
}
