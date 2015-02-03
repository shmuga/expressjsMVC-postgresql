# Livetex-Tools

Build system from LiveTex.

#### Install via npm:
    npm install livetex-tools


## Principles: 

Build system works with artifacts by means of Make.

Project should contain in its root directory a folder **etc/build** with following structure:

    | etc
    `----build  
    |    |----templates  
    |    |    |----js  
    |    |    |    `----*.jst
    |    |    |    `----test-*.jst 
    |    |    `----css  
    |    |         `----*.csst  
    |    `----sources-lists  
    |         |----js  
    |         |    `----*.jsd  
    |         `----css  
    |              `----*.csst  
    ` Makefile  
    
+ **Templates:** \*.jst, \*.csst, test-\*.jst
    ```
    TAG     : %%COMMAND%%    
    COMMAND : any command which can be executed via teminal or make command  
              contained in Makefile  
    !note   : it is preferably to use -s flag with make 
    ```

+ **Sources lists:** *.jsd, *.cssd  
Lists of files that can be used as prerequisites for targets in make  

+ **Makefile:**  
Main file, which includes rules:  
    
    ```
    include node_modules/livetex-tools/rules/web.mk     for web-projects  
    include node_modules/livetex-tools/rules/cpp.mk     for cpp-projects  
    include node_modules/livetex-tools/rules/js.mk      default rules which have  
                                                        to be included the last  
    ```

## Rules: 

+ **For templates**:        
can be used as COMMAND in TAG   

    ```
    syntax: %.extension-prefix
            %         - name of sources list
            extension - js or css
            prefix    - name of action
    ```
    
**js**: js.mk    

    %.js-compile                    :   glues all js files mentioned in sources list  
                                        into single stream and inserts it instead of TAG
                                        
    %.js-compile-compressed         :   compiles and compresses all js files mentioned  
                                        in sources list by means of google-closure-compiler  
                      !note         :   code shouldn`t dependend on any library
                                        
    %.js-externs-compile-compressed :   compiles and compresses all js files mentioned 
                                        in sources list by means of google-closure-compiler   
                                        with externs taken from ./externs folder   
                                        of each dependency (node_modules)
    
**css**: css.mk  

    %.css-compile                   :   compiles all css files mentioned in sources list   
                                        into single stream and inserts it instead of TAG


+ **Main**:   
can be used for one template or sources-list or module

**js**: js.mk

    %.js-lint                       :   checks with google-closure-linter code style
                                        of sources mentioned in sources list
                                        % - name of sources list
    %.js-check                      :   checks syntax with google-closure-compiler
                                        % - name of template
    %.js-assemble                   :   assembles js template to js build path
                                        % - name of template
    %.js-extract-externs            :   extracts externs from built files
                                        % - name of built file
    %.js-test                       :   runs test
                                        % - name of the test
    %.highest-version               :   sets module version to highest version found in npm
                                        % - module name
    %.latest-version                :   sets module version to latest version found in npm
                                        % - module name

**css**: web.mk

    %.css-assemble                  :   assembles css template to css build path
                                        % - name of template


+ **General**:    
can be used as script in NPM  

**js**: js.mk  
    
    js                              :   general rule for js  
    js-lint                         :   checks with google-closure-linter code style of sources  
                                        mentioned in sources lists   
      !note                         :   if you have restrictions for this operation you can list  
                                        only necessary sources lists  
                                        at JS_LINT variable in Makefile
    js-check                        :   checks syntax with google-closure-compiler     
    js-externs                      :   extracts externs from built files   
         !note                      :   if you have restrictions for this operation you can list  
                                        only necessary built files  
                                        at JS_EXTERNS variable in Makefile
    js-build                        :   assembles js templates  
    js-clean                        :   removes built files and externs
    js-tests                        :   runs all tests
    publish                         :   increments patch version, publishes to NPM and pushes tag into GIT  
    
**css**: web.mk     
    
    css                             :   general rule for css  
    css-build                       :   assembles css templates  
    css-clean                       :   removes built files  
    
**cpp**: cpp.mk   
    
    cpp                             :   general rule for cpp  
    cpp-build                       :   moves files built by means of node-gyp into built path and  
                                        removes all node-gyp extra data  
    cpp-clean                       :   removes built files  
    !note                           :   cpp rules have to be used after node-gyp build/rebuild commands  
    
    
## License

Modified BSD License
