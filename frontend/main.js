let projectsUrl = "http://127.0.0.1:8000/api/projects/";

let getProjects = () => {
  fetch(projectsUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      buildProjects(data);
    });
};

getProjects();

let buildProjects = (projects) => {
  let projectsWrapper = document.getElementById("projects-wrapper");

  for (let i = 0; projects.length > i; i++) {
    let project = projects[i];
    console.log(project);
  }
};
