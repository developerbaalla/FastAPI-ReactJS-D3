import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const baseURL = "http://127.0.0.1:8000";


const Graph1 = () => {

	const d3Chart = useRef();

	useEffect(()=>{
		fetch(`${baseURL}/sentence_keywords`)
			.then(response => response.json())
			.then(_data=>{
        
        const nodes = [], links = []; 
        _data.forEach(element => {
          nodes.push({"id": element.sentence, "group": 2});
          element.sentence_keywords.forEach(key => {
            if (!nodes.some(e => e.id === key.value)) {
              nodes.push({"id": key.value, "group": 1});
            }
            links.push({"source": key.value, "target": element.sentence, "value": 1});
          });
        });

        const data = {"nodes": nodes, "links": links};
        
        // set the dimensions and margins of the graph
				const margin = {top: 30, right: 100, bottom: 30, left: 100}
				const width = parseInt(d3.select('#d3demo').style('width')) - margin.left - margin.right
				const height = 550 - margin.top - margin.bottom

        // Set up chart
        const svg = d3.select(d3Chart.current)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)

        const color = d3.scaleOrdinal().range(["red", "green", "blue", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
        const simulation = d3.forceSimulation()
              // Connect edges
              .force('link', d3.forceLink().id(function(d) { return d.id; }))
              // The instance center
              .force('center', d3.forceCenter(width / 2, height / 2))
              // Gravitation
              .force('charge', d3.forceManyBody().strength(-20))
              // Collide force to prevent nodes overlap
              .force('collide',d3.forceCollide().radius(60).iterations(2));


          const link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });
        
          const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(data.nodes)
            .enter().append("g")
        
          const circles = node.append("circle")
            .attr("r", function(d) { return d.group == 1? 4: 6; })
            .attr("fill", function(d) { return color(d.group); });
        
          // Create a drag handler and append it to the node object instead
          const drag_handler = d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended);
        
          drag_handler(node);
          
          const lables = node.append("text")
              .text(function(d) {
                return (d.id.length > 15)? d.id.substring(0,15)+'...': d.id;
              })
              .attr('x', 8)
              .attr('y', 3);
        
          node.append("title")
              .text(function(d) { return d.id; });
        
          simulation
              .nodes(data.nodes)
              .on("tick", ticked);
        
          simulation.force("link")
              .links(data.links);
        
          function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        
            node
                .attr("transform", function(d) {
                  return "translate(" + d.x + "," + d.y + ")";
                })
          }
        // });
        
        function dragstarted(event, d) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }
        
        function dragged(event, d) {
          d.fx = event.x;
          d.fy = event.y;
        }
        
        function dragended(event, d) {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }



			})
	},[])

	return (
		<div id='d3demo'>
			<svg ref={d3Chart}></svg>
		</div>
	)
}

export default Graph1;