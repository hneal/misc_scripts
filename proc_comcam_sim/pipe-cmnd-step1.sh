pipetask run -b /repo/ops-rehearsal-3-prep -i u/jchiang/bfk_50240117_w_2024_04,refcats,skymaps -o u/homer/DM-42862/pipeline_test2 -p pipelines/DRP-ops-rehearsal-3-hn2.yaml#step1,step2a,step2b,step2d,step2e,step3,step4,step5,step6,step7  -d "exposure=5024032100061 AND  detector=0 AND skymap='DC2'" --register-dataset-types
