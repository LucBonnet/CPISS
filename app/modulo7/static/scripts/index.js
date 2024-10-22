const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const rank_persons = document.getElementById("rank-persons")

class App {
  constructor(graph, connections) {
    this.graph = graph;
    this.connections = connections;
    this.personsIds = {};
    this.currentPath = [];

    this.nodeRadius = 30;
    this.width = canvas.width;
    this.height = canvas.height;

    this.margin = this.nodeRadius * 2;
    this.bgColor = "#fff";
    this.nodeColor = "#2C4C7C"
    this.pathColor = "#f00";

    this.showingPath = false;

    this.mouseClicked = false;
    this.mouseMoving = false;

    this.initialX = 0;
    this.initialY = 0;

    this.dx = 0;
    this.dy = 0;

    this.main();
  }

  main() {
    this.clearCanvas();

    this.mapPersons();
    this.formatPersons();
    this.formatConnections();
    this.createNav();

    canvas.addEventListener('click', this.onCanvasClick);

    requestAnimationFrame(() => this.update());
  }

  findNodeByPosition(x, y) {
    
  }

  onCanvasClick(evt) {

  }

  mapPersons() {
    this.graph.forEach((person, index) => {
      this.personsIds[person.id] = index
    });
  }

  formatPersons() {
    for(const person of this.graph) {
      const pos = person.position;
      const x = pos.x + 1;
      const y = pos.y + 1;
  
      const newX = x * this.width / 2;
      const newY = this.height - y * this.height / 2;
      
      person.position = {
        x: Math.min(Math.max(this.margin, newX), this.width - this.margin),
        y: Math.min(Math.max(this.margin, newY), this.height - this.margin),
      }

      person.path = false;
    }
  }

  formatConnections() {
    for(const conn of this.connections) {
      conn.path = false;
    }
  }

  formatImportance(value) {
    const newValue = (value * 100).toFixed(2);
    return `${newValue}%`.replace(".",  ",");
  }

  async calcPath(id) {
    const request = await fetch(`/api/path/${id}`);
    
    if(!request.ok) return;

    if(this.showingPath) return;

    this.showingPath = true;

    const data = await request.json();

    for(const p of this.graph) {
      p.path = false;
    }
    
    for(const c of this.connections) {
      c.path = false;
    }

    let lastPerson = null;
    for(const id of data) {
      this.graph[this.personsIds[id]].path = true;
      
      if (lastPerson == null) {
        lastPerson = id;
        // await new Promise(resolve => setTimeout(resolve, 750 / data.length));
        continue;
      }
      
      for (const conn of this.connections) {
        if(conn.id_person_a == id && conn.id_person_b == lastPerson || conn.id_person_a == lastPerson && conn.id_person_b == id) {
          conn.path = true;
          break;
        }
      }

      // await new Promise(resolve => setTimeout(resolve, 750 / data.length));
      
      lastPerson = id;
    }

    this.showingPath = false;
  }

  createNav() {
    const persons = this.graph.sort((p1, p2) => p2.importance - p1.importance);

    for(let i = 0; i < persons.length; i++) {
      const p = persons[i];

      const content = document.createElement("div");
      content.style.display = "contents";

      const pos_span = document.createElement("span");
      const name_span = document.createElement("span");
      const imp_span = document.createElement("span");
      
      name_span.classList.add("p-name");
      imp_span.style.textAlign = "right";
      pos_span.style.textAlign = "right";

      pos_span.innerText = `${(i + 1)}.`;
      name_span.innerText = p.name;
      imp_span.innerText = this.formatImportance(p.importance);

      content.appendChild(pos_span);
      content.appendChild(name_span);
      content.appendChild(imp_span);

      content.addEventListener('click', (evt) => {
        this.calcPath(p.id);
      });

      rank_persons.appendChild(content);

    }
  }

  clearCanvas() {
    ctx.fillStyle = this.bgColor;
    // ctx.translate(-this.initialX, -this.initialY);
    ctx.fillRect(0, 0, this.width, this.height);
  }

  drawNode(x, y, p) {
    let fillColor = this.nodeColor;
    if(p.path) {
      fillColor = this.pathColor;
    }

    ctx.strokeStyle = "#000";

    ctx.beginPath();
    ctx.arc(x, y, this.nodeRadius, 0, 2 * Math.PI);
    ctx.fillStyle = fillColor;
    const lineWidth = ctx.lineWidth;
    ctx.lineWidth = this.nodeRadius / 10;
    ctx.fill(); 
    ctx.stroke()
    ctx.closePath();

    ctx.lineWidth = lineWidth;
    
    if (!p.name && !p.importance) return; 
  }

  drawNodes() {
    for(const person of this.graph) {
      const pos = person.position;
      this.drawNode(pos.x , pos.y, person);
    }
  }

  drawNodesLabels() {
    for(const person of this.graph) {
      if(!person.name && !person.importance) continue;
      
      const pos = person.position;
      this.drawNodeLabel(pos.x , pos.y, person);
    }
  }

  drawNodeLabel(x, y, p) {
    let fillColor = "#000";
    let bold = "";
    if(p.path) {
      fillColor = this.pathColor;
      bold = "bold";
    }
    ctx.fillStyle = fillColor
    const imp = this.formatImportance(p.importance);
    const label = `${p.name} - ${imp}`;
    const textSize = ctx.measureText(label).width;
    ctx.font = `${bold} ${this.nodeRadius / 2}px "Verdana"`
    ctx.fillText(label, x - (textSize / 2), y + this.nodeRadius * 1.5);
  }


  drawConnection(x0, y0, x1, y1, conn) {
    let color = "#000"
    if(conn.path) {
      color = this.pathColor;
    }
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();
    ctx.closePath();
  }

  drawConnections() {
    for(const conn of this.connections) {
      const id_a = conn.id_person_a;
      const pos_a = this.graph[this.personsIds[id_a]].position;

      const id_b = conn.id_person_b;
      const pos_b = this.graph[this.personsIds[id_b]].position;

      this.drawConnection(pos_a.x, pos_a.y, pos_b.x, pos_b.y, conn);
    }
  }

  update() {
    this.clearCanvas();

    this.drawConnections();
    this.drawNodes();
    this.drawNodesLabels();

    requestAnimationFrame(() => this.update());
  }
}

window.onload = async () => {
  const graph_request = await fetch(`/api/graph`);
  const connections_request = await fetch(`/api/connections`);

  if (graph_request.ok && connections_request.ok) {
    const g_data = await graph_request.json();
    const c_data = await connections_request.json();

    const app = new App(g_data, c_data);
  }
}; 

