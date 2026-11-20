import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {finalizePresentation} from 'file:///C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations/container_tools/artifact_tool_utils.mjs';
process.env.RUNTIME_NODE_MODULES='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const build=path.dirname(fileURLToPath(import.meta.url)), workspaceDir=path.dirname(build);
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations';
const r=await finalizePresentation({workspaceDir,candidatePath:path.join(build,'candidate.pptx'),finalPath:path.join(workspaceDir,'entrega/Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx'),
pythonExecutable:'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','17'],
explicitTotalSlideCount:23,requiredNativeTableOwnerSlides:[17],requiredNativeChartOwnerSlides:[2,4,5,7,8,12,13,16,18],
materializeLiteralChartWorkbooks:false,fontPolicy:{basis:'reference',families:['Arial'],referencePath:path.resolve(workspaceDir,'../apresentacao_banca_v010_visual/entrega/Apresentacao_ESNAUTO_banca_visual_v010.pptx'),referenceSha256:'2be34ffb858391f2c0011f9683cb215adcfc520f7b58fcabed3ce9672ee62b3d'},verifyArtifactToolImport:true,receiptPath:path.join(build,'validacao_final.json')});
console.log('Finalizado',r.finalPath,r.finalSha256);
