/**
 * Displays project tags that are separated by a middle dot.
 * 
 * @param {Object} props - Component properties.
 * @param {string[]} [props.tags=[]]-  The list of project tags to display.
 * @returns 
 */

export default function ProjectTags({ tags = [] }){
    
    const projectTextTags = tags.join (' · ');
    
    return <p>{projectTextTags}</p>;
}   